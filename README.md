# Estimate-Model
Time and cost model for projects with story point size classifications

Software projects of the same estimated size take different periods of time to complete by the same programmer.

However, predicting the delivery time and the total cost of projects allows investors to quantify their capital risks.

This basic Monte Carlo model assumes
- the time/cost to complete each user story can be based on a Gamma random variable and the story's size
- The mean time for one programmer to complete a one story point task is one time unit.
- User story point sizes are linear   ie Time(a+ b) = Time(a) + Time(b)
- there is no co-ordination wastage when more programmers are added to a project
- all programmers have the same skill level

The model runs tests
- for 100 story points as 100x1, random story point tasks summing to 100 & random story point tasks summing to 100 ordered by descending size
- with one, five and ten programmers working on the same backlog
- with programmers simultaneously working independently on the same task item when the backlog has no unassigned tasks remaining.

Results are quoted in probability bands

## MEANS   
Duration:         μ 12.44 (σ 2.14 /0.17)   
Cost/planned usp: μ 1.24 (σ 0.21 /0.17)   
Adj cost/usp:     μ 1.20 (σ 0.19 /0.16)   
Assigned:         μ 69.00 (σ 13.52 /0.20)   
Unassigned        μ 4.68 (σ 6.24 /1.33)   
Waste:            μ 50.75 (σ 13.11 /0.26)   


## PERCENTILES             min      5%      15%     25%   50%    75%     85%     95%     max   
Duration:         <--   7.2 {{   9.3 {  10.4 [  10.9   12.2   13.8 ]  14.7 }  16.2 }}  20.4 -->   
Totals:   
Cost:             <--  72.4 {{  92.7 { 103.5 [ 109.0  122.5  138.1 ] 146.8 } 162.0 }} 204.5 -->   
Assigned:         <--  34.3 {{  49.1 {  55.5 [  59.4   67.5   77.9 ]  83.1 }  92.3 }} 139.5 -->   
UnAssigned:       <--   0.0 {{   0.3 {   0.6 [   0.9    2.2    6.1 ]   9.5 }  16.3 }}  46.4 -->   
Waste:            <--  18.3 {{  31.2 {  38.3 [  41.1   50.1   58.3 ]  63.2 }  75.7 }} 104.3 -->   


## Conclusions
- As expected, adding more programmers substantially reduces the likelihood that a project will overrun in time.
- Applying multiple programmers to the same task will also limit project time overrun, at modest cost.
- Decomposing user stories into stories of size 1, creates a situation where n programmers operate at a similar efficency to 1 programmer but with narrow delivery margins.
