import math
import sys

args = sys.argv

if len(args) < 5:
    print('Incorrect parameters')
    sys.exit()

# payment type
if args[1] == '--type=diff':
    type = 'diff'
elif args[1] == '--type=annuity':
    type = 'annuity'
else:
    print('Incorrect parameters')
    sys.exit()

## differentiated payment
if type == 'diff':
    P = [float(i[12:]) for i in args[2:] if '--principal=' in i]
    n = [int(i[10:]) for i in args[2:] if '--periods=' in i]  
    I = [float(i[11:]) for i in args[2:] if '--interest=' in i]    

    # all 3 parameters (P, n, I) need to be supplied
    if ((not P) or (not n) or (not I)):
        print('Incorrect parameters')
        sys.exit()

    # values cannot be negative
    if (P[0] <= 0) or (n[0] <= 0) or (I[0] <= 0):
        print('Incorrect parameters')
        sys.exit()

    P = P[0]
    I = I[0]
    n = n[0]

    # nominal interest (monthly)
    i = I / (12 * 100)

    # calculate monthly payment D(m)
    total_paid = 0
    for m in range(1, n + 1):
        D = math.ceil((P/n) + i * (P - ((P * (m - 1)) / n)))
        print(f'Month {m}: paid out {D}')
        total_paid += D

    overpayment = round(total_paid - P)
    print(f'Overpayment: {overpayment}')


## annuity payment
if type == 'annuity':
    P = [float(i[12:]) for i in args[2:] if '--principal=' in i]  # credit principal
    n = [int(i[10:]) for i in args[2:] if '--periods=' in i]  # number of periods
    I = [float(i[11:]) for i in args[2:] if '--interest=' in i] # credit interest
    A = [float(i[10:]) for i in args[2:] if '--payment=' in i]  # annuity payment

    # monthly interest
    i = I[0] / (12 * 100)

    # finding number of periods
    if not n:
        n = math.ceil(math.log(A[0] / (A[0] - i * P[0]), 1 + i))
        if n <= 11:
            print('You need {0} months to repay this credit!'.format(n))
        else:
            years = n // 12
            months = n % 12
            if months == 0:
                print('You need {0} years to repay this credit!'.format(years))
            else:
                print('You need {0} years and {1} months to repay this credit!'.format(years, months))

        overpayment = round((n * A[0]) - P[0])
        print(f'Overpayment: {overpayment}')

    # finding principal amount
    if not P:
        P = math.floor(A[0] / ((i * ((1 + i) ** n[0])) / (((1 + i) ** n[0]) - 1)))
        print(f"Your credit principal = {P}!")

        overpayment = round((n[0] * A[0]) - P)
        print(f'Overpayment: {overpayment}')

    # finding annuity payment
    if not A:
        A = math.ceil(P[0] * ((i * ((1 + i) ** n[0])) / (((1 + i) ** n[0]) - 1)))
        print(f'Your annuity payment = {A}!')

        overpayment = round((n[0] * A) - P[0])
        print(f'Overpayment: {overpayment}')
