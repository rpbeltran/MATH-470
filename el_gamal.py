
from primality import is_prime
from powering  import fast_powering, fermat_inverse, extended_euclidean_inverse
from gcd       import euclids_gcd

import random

class ElGamal_Agent:

	# Note: This class is not a secure implementation of El Gamal
	#   but rather a simple implementation to aid in understanding

	default_configuration = {
		'width' : 24 # We use a small width because our generation of g is naive and ths inefficient
	}

	def __init__( self, **configuration ):

		self.configuration = ElGamal_Agent.default_configuration
		self.configuration.update( configuration )

		self.generate_public_key()

	def generate_public_key( self ):

		# Find suitable prime p

		if 'p' in self.configuration:
		
			self.p = self.configuration['p']
		
		else:

			while True:
				self.p = random.randrange( 3, 2<<(self.configuration['width']) )
				if is_prime( self.p ):
					break

		# Select an element g of high order modulo p

		if 'g' in self.configuration:
		
			self.g = self.configuration['g']

		else:

			for g in range( 1, self.p ):

				order = 1

				element = g % self.p

				while (element != 1 ):
					element = (element*g) % self.p
					order += 1

				if ( order >= self.p - 1 ):
					self.g = g
					break

		# Find a suitable private key ( a )

		self.private_key = self.configuration['a'] if 'a' in self.configuration else random.randrange( 1, self.p )

		# Solve for a suitable public key

		self.public_key = fast_powering( self.g, self.private_key, self.p )


	# Public Key Encryption

	def encrypt( self, message, agent ):

		k = random.randrange( 2, agent.p-1 )

		c1 = fast_powering( agent.g, k, agent.p )
		c2 = ( m * fast_powering( agent.public_key, k, agent.p ) ) % agent.p

		return ( c1, c2 )


	def decrypt( self, cryptotext ):

		c1, c2 = cryptotext

		return ( c2 * fermat_inverse( fast_powering( c1, self.private_key, self.p ), self.p ) ) % self.p


	# Document Signing

	def hash_document( self, document ):

		# Note: We are not using a cryptographic hash function
		#   The hash funcition we use is easily reversible
		#   We don't concern ourselves with this as one way hashing
		#   does not get discussed until Chapter 8 in out textbook
		#   The purpose of this hash function is for normalization

		return abs( hash( document ) )

	def sign( self, document, hashing = True ):

		hashed_document = self.hash_document( document )

		while True:
			
			k = random.randrange( 2, self.p-1 )
			
			if euclids_gcd( k, self.p-1 ) == 1:
				break

		s1 = fast_powering( self.g, k, self.p )
		s2 = ( ( hashed_document - self.private_key * s1 ) * extended_euclidean_inverse( k, self.p-1 ) ) % (self.p-1)

		return ( s1, s2 )


	def verify( self, signature, document, agent, hashing = True ):

		hashed_document = self.hash_document( document )

		verification = ( fast_powering( agent.public_key, signature[0], agent.p ) * fast_powering( signature[0], signature[1], agent.p ) ) % agent.p

		return fast_powering( agent.g, hashed_document, agent.p ) == verification



if __name__ == '__main__':
	
	bob   = ElGamal_Agent()
	alice = ElGamal_Agent()

	samantha = ElGamal_Agent()
	victor   = ElGamal_Agent()


	print " --- Encryption ----\n"

	m = 107077
	c = alice.encrypt( m, bob )
	d = bob.decrypt( c )

	print "Bob has a public key (a) = %i" % bob.public_key
	print "Alice wishes to tell Bob the message \"%i\"" % m
	print "Alice encrypts with Bob's public key to generate the cryptotext: (%i, %i)" % c
	print "Bob decrypts the message as \"%d\"\n" % d

	print " --- Document signing ----\n"

	document = "I will take you to Jaba now"

	signature = samantha.sign( document )

	verified = victor.verify( signature, document, samantha )

	print "Samantha writes to Victor that \"%s\" (hash = %i), but he'd feel more comfortable with a signature" % ( document, samantha.hash_document( document) )
	print "Samantha, whose public key (a) = %i agrees" % bob.public_key
	print "Samantha sends him the signature: (%i,%i)" % signature
	print "Victor seeks to verify it.... %s" % ( "VERIFIED" if verified else "FAILURE")











