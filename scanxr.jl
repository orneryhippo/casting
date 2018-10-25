using Memoize
@memoize function sieve(n)
  if n < 2
      return false
  end
  if n % 2 == 0
      return n == 2
  end
  k = 3
  while k*k <= n
      if n % k == 0
          return false
      end
      k += 2
  end
  return true
end


is_prime = sieve
function is_tprime(seed)
    p1 = 6*seed - 1
    return is_prime(p1) && is_prime(p1 + 2)
end

rs = [0,2,3,5,7,10,12,17,18,23,25,28,30,32,33]
rcounts = Dict{Int64,Int64}(r => 0 for r in rs)

function countem(ct = 100)
    rcounts = Dict{Int64,Int64}(r => 0 for r in rs)
    for x in 1:ct+1
        for r in rs
            if is_tprime(35*x + r)
                rcounts[r] += 1
            end
        end
    end
    return rcounts
end
