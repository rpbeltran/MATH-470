
from primality import is_prime
from gcd       import euclids_gcd, extended_euclids_gcd
from powering  import fast_powering

import random

class RSA_Agent:

	# Note: This class is not a secure implementation of RSA
	#   but rather a simple implementation to aid in understanding

	default_configuration = {
		'width' : 64
	}

	def __init__( self, **configuration ):

		self.configuration = RSA_Agent.default_configuration
		self.configuration.update( configuration )

		self.generate_public_key()

	def generate_public_key( self ):

		# Find suitable primes p, and q

		if 'p' in self.configuration:
		
			self.p = self.configuration['p']
		
		else:

			while True:
				self.p = random.randrange( 2, 2<<(self.configuration['width']>>1) )
				if is_prime( self.p ):
					break

		if 'q' in self.configuration:
		
			self.q = self.configuration['q']
		
		else:

			while True:
				self.q = random.randrange( 2, 2<<(self.configuration['width']>>1) )
				if is_prime( self.q ):
					break

		self.pq = self.p*self.q

		# Find a suitable exponent e

		if 'e' in self.configuration:
		
			self.e = self.configuration['e']
		
		else:

			while True:
				
				self.e = random.randrange( 2, 2<<(self.configuration['width']) )
				
				if euclids_gcd( self.e, (self.p-1)*(self.q-1) ) == 1:
					break

		
		# We now have all the pieces for our public key

		self.public_key = ( self.pq, self.e )


		# Solve for inverse of e

		self.d = extended_euclids_gcd( self.e, (self.p-1)*(self.q-1) )[1]

		if self.d < 0:
			self.d += (self.p-1)*(self.q-1)


	# Public Key Encryption

	def encrypt( self, message, agent ):

		key = agent.public_key

		return fast_powering( message, key[1], key[0] )


	def decrypt( self, cryptotext ):

		return fast_powering( cryptotext, self.d, self.pq )


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

		return fast_powering( hashed_document, self.d, self.pq )


	def verify( self, signature, document, agent, hashing = True ):

		hashed_document = self.hash_document( document )

		key = agent.public_key

		return hashed_document == fast_powering( signature, key[1], key[0] )



if __name__ == '__main__':
	
	bob   = RSA_Agent()
	alice = RSA_Agent()

	samantha = RSA_Agent()
	victor   = RSA_Agent()


	print " --- Encryption ----\n"

	m = 1070777
	c = alice.encrypt( m, bob )
	d = bob.decrypt( c )

	print "Bob has a public key (pq,e) = (%i,%i)" % bob.public_key
	print "Alice wishes to tell Bob the message \"%i\"" % m
	print "Alice encrypts with Bob's public key to generate the cryptotext: \"%i\"" % c
	print "Bob decrypts the message as \"%d\"\n" % d

	print " --- Document signing ----\n"

	document = "I will take you to Jaba now"

	signature = samantha.sign( document )

	verified = victor.verify( signature, document, samantha )

	print "Samantha writes to Victor that \"%s\" (hash = %i), but he'd feel more comfortable with a signature" % ( document, samantha.hash_document( document) )
	print "Samantha, whose public key (pq,e) = (%i,%i) agrees" % bob.public_key
	print "Samantha sends him the signature: %i" % signature
	print "Victor seeks to verify it.... %s" % ( "VERIFIED" if verified else "FAILURE")











