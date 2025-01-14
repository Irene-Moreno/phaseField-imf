#include "../../include/matrixFreePDE.h"

template <int dim, int degree>
class customPDE: public MatrixFreePDE<dim,degree>
{
public:
    // Constructor
    customPDE(userInputParameters<dim> _userInputs): MatrixFreePDE<dim,degree>(_userInputs) , userInputs(_userInputs) {};

    // Function to set the initial conditions (in ICs_and_BCs.h)
    void setInitialCondition(const dealii::Point<dim> &p, const unsigned int index, double & scalar_IC, dealii::Vector<double> & vector_IC);

    // Function to set the non-uniform Dirichlet boundary conditions (in ICs_and_BCs.h)
    void setNonUniformDirichletBCs(const dealii::Point<dim> &p, const unsigned int index, const unsigned int direction, const double time, double & scalar_BC, dealii::Vector<double> & vector_BC);

private:
	#include "../../include/typeDefs.h"

	const userInputParameters<dim> userInputs;

	// Function to set the RHS of the governing equations for explicit time dependent equations (in equations.h)
    void explicitEquationRHS(variableContainer<dim,degree,dealii::VectorizedArray<double> > & variable_list,
					 dealii::Point<dim, dealii::VectorizedArray<double> > q_point_loc) const;

    // Function to set the RHS of the governing equations for all other equations (in equations.h)
    void nonExplicitEquationRHS(variableContainer<dim,degree,dealii::VectorizedArray<double> > & variable_list,
					 dealii::Point<dim, dealii::VectorizedArray<double> > q_point_loc) const;

	// Function to set the LHS of the governing equations (in equations.h)
	void equationLHS(variableContainer<dim,degree,dealii::VectorizedArray<double> > & variable_list,
					 dealii::Point<dim, dealii::VectorizedArray<double> > q_point_loc) const;

	// Function to set postprocessing expressions (in postprocess.h)
	#ifdef POSTPROCESS_FILE_EXISTS
	void postProcessedFields(const variableContainer<dim,degree,dealii::VectorizedArray<double> > & variable_list,
					variableContainer<dim,degree,dealii::VectorizedArray<double> > & pp_variable_list,
					const dealii::Point<dim, dealii::VectorizedArray<double> > q_point_loc) const;
	#endif

	// Function to set the nucleation probability (in nucleation.h)
	// #ifdef NUCLEATION_FILE_EXISTS
	double getNucleationProbability(variableValueContainer variable_value, double dV, dealii::Point<dim> p, unsigned int variable_index) const;
	// #endif

	// ================================================================
	// Methods specific to this subclass
	// ================================================================

	// Method to place the nucleus and calculate the mobility modifier in residualRHS
	void seedNucleus(const dealii::Point<dim, dealii::VectorizedArray<double> > & q_point_loc,
						dealii::VectorizedArray<double> & source_term,
						dealii::VectorizedArray<double> & gamma) const;

	// ================================================================
	// Model constants specific to this subclass
	// ================================================================

	double Mc = userInputs.get_model_constant_double("Mc");
	double Mn = userInputs.get_model_constant_double("Mn");
	double Kn = userInputs.get_model_constant_double("Kn");
	double calmin = userInputs.get_model_constant_double("calmin"); // from nucleation app

    dealii::Tensor<1,dim> center1 = userInputs.get_model_constant_rank_1_tensor("center1");
    dealii::Tensor<1,dim> center2 = userInputs.get_model_constant_rank_1_tensor("center2");

    double radius1 = userInputs.get_model_constant_double("radius1");
    double radius2 = userInputs.get_model_constant_double("radius2");

    double matrix_concentration = userInputs.get_model_constant_double("matrix_concentration");

	double k1 = userInputs.get_model_constant_double("k1");  // all these from nucleation app
	double k2 = userInputs.get_model_constant_double("k2");
	double tau = userInputs.get_model_constant_double("tau");
	double epsilon = userInputs.get_model_constant_double("epsilon");

	// Interface coefficient
	// Originally not defined in CHAC, but needed for seedNucleus. Given the equations shape, this
	// expression for it is what makes most sense for me (or kappa, directly). 
	double interface_coeff = std::sqrt(2.0*Kn);


	// ================================================================

};
