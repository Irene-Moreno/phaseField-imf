//constructor and destructor for matrixFreePDE class

#ifndef MATRIXFREEPDE_MATRIXFREE_H
#define MATRIXFREEPDE_MATRIXFREE_H
//this source file is temporarily treated as a header file (hence
//#ifndef's) till library packaging scheme is finalized

#include "../../include/matrixFreePDE.h"


 //constructor
template <int dim, int degree>
 MatrixFreePDE<dim,degree>::MatrixFreePDE (userInputParameters _userInputs)
 :
 Subscriptor(),
 userInputs(_userInputs),
 triangulation (MPI_COMM_WORLD),
 isTimeDependentBVP(false),
 isEllipticBVP(false),
 currentTime(0.0),
 currentIncrement(0),
 pcout (std::cout, Utilities::MPI::this_mpi_process(MPI_COMM_WORLD)==0),
 computing_timer (pcout, TimerOutput::summary, TimerOutput::wall_times),
 energy(0.0),
 parabolicFieldIndex(0),
 ellipticFieldIndex(0),
 currentFieldIndex(0),
 num_quadrature_points(1)
 { }

 //destructor
 template <int dim, int degree>
 MatrixFreePDE<dim,degree>::~MatrixFreePDE ()
 {
   matrixFreeObject.clear();
   for(unsigned int iter=0; iter<fields.size(); iter++){
     delete soltransSet[iter];
     delete locally_relevant_dofsSet[iter];
     delete constraintsDirichletSet[iter];
     delete dofHandlersSet[iter];
     delete FESet[iter];
     delete solutionSet[iter];
     delete residualSet[iter];
   } 
 }

 // Template instantiation
 //template class MatrixFreePDE<1>; // Issue with the destructor if I include the dim=1 template
 //template class MatrixFreePDE<2>;
 //template class MatrixFreePDE<3>;

//#include "init.cc"
//#include "reinit.cc"
//#include "initForTests.cc"
//#include "refine.cc"
//#include "invM.cc"
//#include "computeLHS.cc"
//#include "computeRHS.cc"
//#include "modifyFields.cc"
//#include "solve.cc"
//#include "solveIncrement.cc"
//#include "outputResults.cc"
//#include "markBoundaries.cc"
//#include "boundaryConditions.cc"
//#include "initialConditions.cc"
//#include "utilities.cc"
//#include "calcFreeEnergy.cc"
//#include "integrate_and_shift_field.cc"
//#include "getOutputTimeSteps.cc"
//#include "buildFields.cc"

#ifndef MATRIXFREEPDE_TEMPLATE_INSTANTIATION
#define MATRIXFREEPDE_TEMPLATE_INSTANTIATION
template class MatrixFreePDE<2,1>;
template class MatrixFreePDE<3,1>;
#endif



#endif
