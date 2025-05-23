def quick_mod(large_base, large_exponent, mod):
    
    binary_exponent = bin(large_exponent)[2:][::-1]
    multiplier_list = [large_base % mod]
    product = 1

    for i in range(1, len(binary_exponent)):
        multiplier_list.append((multiplier_list[-1] ** 2) % mod)
        if binary_exponent[i] == '1':
            product *= multiplier_list[-1]
    
    if binary_exponent[0] == '1':
        product *= large_base
    return product % mod


large_base = 1
large_exponent = 43
mod = 85

print(f'{large_base} to the {large_exponent} % {mod} = {quick_mod(large_base, large_exponent, mod)}')