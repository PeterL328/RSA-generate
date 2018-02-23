#!/usr/bin/python
# =======================================================================================================
# Code: ECE 103 optional assignment for lazy people
# Description: Extra assignment
#
# Built for Python 2.7.6 (Works on Python 2.6 and 2.7)
# Date: March 12, 2016
#
# Programmer: Peter Leng
# ======================================================================================================

# Library
import random
import math
# Variables
numberOfBits = 1023  # you can change this to generate a certain amount of digits
maxTries = 10  # of tries you can repeat input data if exception is found


# Functions
def rabinMiller(n):
	s = n - 1
	t = 0
	while s & 1 == 0:
		s = s / 2
		t += 1
	k = 0
	while k < 128:
		a = random.randrange(2, n - 1)
		# a^s is computationally infeasible.  we need a more intelligent approach
		# v = (a**s)%n
		# python's core math module can do modular exponentiation
		v = pow(a, s, n)  # where values are (num,exp,mod)
		if v != 1:
			i = 0
			while v != (n - 1):
				if i == t - 1:
					return False
				else:
					i = i + 1
					v = (v**2) % n
		k += 2
	return True


def isPrime(n):
	# lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
	# under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
	# of composite numbers from our potential pool without resorting to Rabin-Miller
	lowPrimes = [
		3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
		79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
		163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239,
		241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331,
		337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
		431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509,
		521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613,
		617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
		719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821,
		823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919,
		929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
	]
	if (n >= 3):
		if (n & 1 != 0):
			for p in lowPrimes:
				if (n == p):
					return True
				if (n % p == 0):
					return False
			return rabinMiller(n)
	return False


def generateLargePrime(k):
	# k is the desired bit length
	r = 100 * (math.log(k, 2) + 1)  # number of attempts max
	while r > 0:
		# randrange is mersenne twister and is completely deterministic
		# unusable for serious crypto purposes
		n = random.randrange(2**(k - 1), 2**(k))
		r -= 1
		if isPrime(n):
			return n
	return -1  # "Failure after "+`r_` + " tries."


def gcd(a, b):
	if b > a:
		return gcd(b, a)

	if a % b == 0:
		return b

	return gcd(b, a % b)


# EEA
def egcd(a, b):
	x, y, u, v = 0, 1, 1, 0
	while a != 0:
		q, r = b // a, b % a
		m, n = x - u * q, y - v * q
		b, a, x, y, u, v = a, r, u, v, m, n
	return x


def asciiToText(d_msg):
	# add 0's to the front if this is not a multiple of 3
	while len(d_msg) % 3 != 0:
		d_msg = "0" + d_msg
	list = [int(d_msg[i:i + 3]) for i in range(0, len(d_msg), 3)]
	for l in list:
		if l > 256:
			print "Some values are greater then 256 which is out of range for ASCII. Exiting..."
			quit()
	plain_text = ''.join(chr(i) for i in list)
	return plain_text


def addZeros(c):
	while len(c) % 3 != 0:
		c = "0" + c
	return c


def squareAndMultiply(base, exponent, modulus):
	# Converting the exponent to its binary form
	binaryExponent = []
	while exponent != 0:
		binaryExponent.append(exponent % 2)
		exponent = exponent / 2

	# Appllication of the square and multiply algorithm

	result = 1
	binaryExponent.reverse()
	for i in binaryExponent:
		if i == 0:
			result = (result * result) % modulus
		else:
			result = (result * result * base) % modulus

			# print i,"\t",result
	return result


def mainProgram():
	print "To use this program, you may first generate a key with (g), then run the program with (e) to encrypt a message and (d) to decrypt a message. \n"

	try:
		while(True):
			try:
				prog = raw_input("Select to encrypt, decrypt or generate key?(e/d/g): ")
			except EOFError:
				quit()
			# Encryption
			if prog == 'e':
				# ask for the receiver's variable
				try:
					n = long(raw_input("Enter n value: "))
					print "\n"
					e = long(raw_input("Enter e value: "))
					print "\n"
					# Ask for message
					msg = raw_input("Enter your message: ")
				except ValueError:
					print "Invalid input"
					quit()
				except OverflowError:
					print "Value entered exceeded the maximum limit"
					quit()
				except EOFError:
					quit()
	
				msg_ascii = long(''.join(addZeros(str(ord(c))) for c in msg))
				print "Your message in ASCII is: ", msg_ascii, "\n"
	
				# Encryption
				c = squareAndMultiply(msg_ascii, e, n)
				print "Your encrypted text is: ", c, "\n"
	
			# Decryption
			elif prog == 'd':
				try:
					c_sender = long(raw_input("Enter encrypted text value: "))
					print "\n"
					d_yours = long(
						raw_input(
							"Enter your d value (This can be generated with the 'g' option): "))
					print "\n"
					n_yours = long(
						raw_input(
							"Enter your n value (This can be generated with the 'g' option): "))
					print "\n"
				except OverflowError:
					print "Value entered exceeded the maximum limit"
					quit()
				except ValueError:
					print "Invalid input"
					quit()
				except EOFError:
					quit()
					# decrypt value
				msg_decrypt = str(squareAndMultiply(c_sender, d_yours, n_yours))
				print "The decrypted values is: ", msg_decrypt, "\n"
	
				print "Changing to ASCII...\n"
				print "The message is: ", asciiToText(msg_decrypt)  # Generate Key
			elif prog == 'g':  # Ask for input for key creation
				print "Generating a 300 digit p and q value and picking an e value."
				print "Calculating... \n"
				# p & q
				p = generateLargePrime(numberOfBits)
				while p == -1:
					p = generateLargePrime(numberOfBits)
				q = generateLargePrime(numberOfBits)
				while q == -1:
					q = generateLargePrime(numberOfBits)
				# n
				n = q * p
				# phi
				phi = (q - 1) * (p - 1)
				# e
				e = generateLargePrime(17)
				e_test = gcd(phi, e)
				# keeping picking e valie until gcd is 1
				while e_test != 1:
					e = generateLargePrime(17)
					e_test = gcd(phi, e)
	
				# d
				d = egcd(e, phi)
				# if d is a negative number we add phi to it
				if d < 0:
					d += phi
				print "p = ", p, "\n"  # 1023 is the default bit length. It generates a number with about 300 digits.
				print "q = ", q, "\n"
				print "phi =", phi, "\n"
				print "e = ", e, "\n"
				print "n = ", n, "\n"
				print "d = ", d, "\n"  # Exit
			else:
				print "Wrong input. Exiting..."
	except KeyboardInterrupt:
		quit()  # run main

if __name__ == '__main__':
	mainProgram()

