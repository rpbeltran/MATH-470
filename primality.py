
import random



def miller_rabin ( n, a ): # True implies n is composite

	from gcd import euclids_gcd

	# Test if n is even
	if not( n & 1 ):
		return True

	# Test if a divides n
	gcd = euclids_gcd( n, a )

	if (1 < gcd ) and ( gcd < n ):
		return True

	# Find q such that n - 1 = 2^k q

	q = n - 1
	k = 0
	while not( q & 1 ):
		q >>= 1
		k  += 1

	# Search for the existence of i such that a^( (2^i) q ) = -1 (mod p), i < k
	a = pow( a, q, n )

	if a == 1:
		return False

	for i in range( k ):

		if a == n-1:

			return False

		a = pow( a, 2, n )

	return True



def is_prime( n, rounds = 100 ):

	if n == 1:   return False
	elif n == 2: return True

	for _ in range( rounds ):

		a = random.randrange( 2, n )

		if miller_rabin( n, a ):
			return False

	return True

