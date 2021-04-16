#import Pkg
#Pkg.add("StatsBase")
using StatsBase

function find_cycle(g, chain)
    head = chain[end]
    if length(chain) > 1
        last = chain[end-1]
        neis = []
        for i in g[head]
            if i != last
                push!(neis, i)
            end
        end
    else
        neis = collect(g[head])
    end
    while true
        next = sample(neis)
        # println(next)
        if in(next, chain)
            # rec = indexin(next, chain)
            rec=0
            for i in 1:length(chain)
                if chain[i] == next
                    rec = i
                    break
                end
            end
            cycle = collect(view(chain, rec:length(chain)))
            tail  = collect(view(chain, 1:rec-1))
            return tail, cycle
        end
        push!(chain, next)
        last = chain[end-1]
        neis = []
        for i in g[next]
            if i != last
                push!(neis, i)
            end
        end
    end
end
# 書けたっぽい!

function tileByCycles(g)
    cycles = Array([])
    chain  = Array([])
    while length(g) > 0
        if length(chain) == 0
            L = collect(keys(g))
            head = sample(L)
            chain = Array([head])
        end
        # println("chain",chain)
        chain, cycle = find_cycle(g, chain)
        # println(cycle)
        push!(cycles, cycle)
        for i in 1:length(cycle)
            ii = i - 1
            if ii == 0
                ii = length(cycle)
            end
            a = cycle[ii]
            b = cycle[i]
            # println("remove edge",a,b)
            # remove edge from g
            pop!(g[a], b)
            pop!(g[b], a)
        end
        for a in cycle
            if length(g[a]) == 0
                pop!(g, a)
            end
        end
        # println(g)
    end
    return cycles
end


# どうにか書いたけど、Juliaは完全なコンパイラ言語ではなくJITだったらしい。うーむむむむ。
# このコードを、辞書を使わずに高速に書けるか???
# 今日はあきらめる。

g = Dict(1=>Set([2,3,4,5]),
         2=>Set([1,3,4,6]),
         3=>Set([1,2,5,6]),
         4=>Set([1,2,5,6]),
         5=>Set([1,3,4,6]),
         6=>Set([2,3,4,5]))

# chain = Array([1,2])
# tail, cycle = find_cycle(g, chain)
# println("tail")
# println(tail)
# println("cycle")
# println(cycle)

cycles = tileByCycles(g)
println(cycles)
