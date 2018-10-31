

def euclids_gcd( a, b ):

    if b > a:
        a, b = b, a

    while a % b != 0:

        a, b = b, a % b

    return b


def extended_euclids_gcd( a, b ):

    reverse = b > a

    if reverse:
        a, b = b, a

    d = []
    while True:

        d.append( int( a / b ) )

        if( a % b == 0 ):
            break

        a, b = b, a % b

    t = len( d )

    #calculate u
    
    u = reduce( lambda acc, i : ( acc[1], acc[0] + acc[1] * i ), d, (1,0) ) [0]
    u = u if not t % 2 else -u

    #calculate v
    
    v = -1 * reduce( lambda acc, i : ( acc[1], acc[0] + acc[1] * i ), d, (0,1) ) [0]
    v = v if not t % 2 else -v

    return ( b, u, v ) if not reverse else ( b, v, u )

if __name__ == '__main__':
    
    print extended_euclids_gcd( 948047, 1222 )