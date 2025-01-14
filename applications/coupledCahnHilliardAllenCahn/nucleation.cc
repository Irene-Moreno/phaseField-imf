// =================================================================================
// NUCLEATION FUNCTIONS
// =================================================================================

// =================================================================================
// Nucleation probability
// =================================================================================

// NOTE: there are many constants that were defined in the nucleation app, where this fcn comes from, 
// that weren't defined in CHAC originally. 
template <int dim, int degree>
double customPDE<dim,degree>::getNucleationProbability(variableValueContainer variable_value, double dV, dealii::Point<dim> p, unsigned int variable_index) const
{
	//Supersaturation factor
    double ssf;
    if (dim ==2) ssf=variable_value(0)-calmin;
    if (dim ==3) ssf=(variable_value(0)-calmin)*(variable_value(0)-calmin);
	// Calculate the nucleation rate
	double J=k1*exp(-k2/(std::max(ssf,1.0e-6)))*exp(-tau/(this->currentTime));
	double retProb=1.0-exp(-J*userInputs.dtValue*((double)userInputs.steps_between_nucleation_attempts)*dV);
    return retProb;
}
