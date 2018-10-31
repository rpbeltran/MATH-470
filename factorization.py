
from gcd       import euclids_gcd
from primality import is_prime

def pollards ( N, attempts = 100, a_max = 13 ):

	# We seek p, q such that pq = N
	# We notice that a^(p-1)i = 1 modulo p for all integers i
	# 	 and that it is rather unlikely that a^(p-1)i = 1 modulo q
	# We see that this statement is equivalent to:
	#    "p divides a^(p-1)i-1, but q probably does not divide a^(p-1)i-1"
	# We therefore seek L such that p divides a^L - 1, but q does not divide A^L-1
	# If p-1 is a product of small prime, we will probably discover p-1 | n! for some small n
	# Therefore, we realise that, if p-1 is the product of small primes, a suitable L is n! for some small n

	for a in range( 2, a_max + 1 ):

		trial_L = 1
		trial   = 1

		for i in range( 1, attempts ):

			trial_L *= i
			trial_L %= N

			trial **= (N-1)

			trial = pow( a, trial_L, N ) - 1

			if trial < 1:
				trial += N

			gcd = euclids_gcd( N, trial)

			if( gcd == N ): 
				break

			if( gcd != 1 ):
				return (gcd, N/gcd)


def naive_difference_of_squares_factorization ( n, outer_depth = 1000, inner_depth = 1000, verbose = False ):

	is_square = lambda x, float_precision = 1e-12 : int( x**.5 + float_precision ) ** 2 == x

	k = 1

	if n == 1 or is_prime( n ): return [ n ]

	for _ in range( outer_depth ):

		k += 1 if not n % 2 else 2

		for b in range( inner_depth ):

			if is_square( k*n + b**2 ):

				a = int( round( (k*n + b**2)**.5 ) )

				f1 = euclids_gcd( n, a + b )
				f2 = euclids_gcd( n, a - b )

				if (f1 in [1,n]) and (f2 in [1,n]):
					continue

				elif (f1 in [1,n]):
					f1 = n / f2
				
				elif (f2 in [1,n]):
					f2 = n / f1

				elif f1 * f2 != n:
					f1 = max( f1, f2 )
					f2 = n / f1

				if verbose:
					print str(n) + " => " + str([f1,f2])

				return sorted( naive_difference_of_squares_factorization( f1 ) + naive_difference_of_squares_factorization( f2 ) )

	# No solution found in given depth
	return [ n ]


if __name__ == '__main__':

	print naive_difference_of_squares_factorization( 90830 )




