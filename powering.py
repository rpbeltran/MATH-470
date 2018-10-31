
def fermat_inverse( a, m ):

	# Note: this only works if m is prime
	
	return fast_powering( a, m-2, m )


def extended_euclidean_inverse( a, m ):

	# Note: this only works if a does not divide b

	from gcd import extended_euclids_gcd

	extended_gcd = extended_euclids_gcd( a, m )

	assert extended_gcd[0] == 1

	return extended_gcd[1]


def fast_powering( base, power, m ):

	# Note: this is equivalent to pow( base, power, m )

	assert ( power >= 0 )

	result = 1

	while ( power > 0 ):

		if ( power & 1 ): 
			result = (result*base) % m

		base = ( base**2 ) % m

		power >>= 1

	return result