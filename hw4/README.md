# HW4: ETF評比績效理論實作 :
---
### Demo

* 週資料分析組
---
![image](https://github.com/b05902109/Fintech_TM-ML/blob/master/hw4/week_rank.PNG)

* 月資料分析組 
---
![image](https://github.com/b05902109/Fintech_TM-ML/blob/master/hw4/month_rank.PNG)


### 資料欄位說明
---
#### 1. ASSR_week_b2_rank (ASSR_month_b2_rank) ;  ASSR_week_b1_rank (ASSR_month_b1_rank)
---
* Both calculated by the formula (20) in Portfolio performance evaluation with generalized Sharpe ratios: Beyond the mean and variance (2009)
* b2 represents investors with logarithmic utility (closer to the real financial market)
* b1 represents investors with CARA utility

#### 2. Sharpe_Omega_week_rank (Sharpe_Omega_month_rank)
---
* Calculated by the formula (8) in Omega performance measure and portfolio insurance (2011)

#### 3. Riskiness_week_uniform_rank (Riskiness_month_uniform_rank) ; Riskiness_week_fitpdf_rank (Riskiness_month_fitpdf_rank)
---
* Both calculated by the formula in A global index of riskiness (2013) P.494 Q(g)
* uniform means using uniform distribution to calculate the expected value
* fitpdf means using ETF's own probability density function to calculate the expected value

### 週資料或月結果評比相似嗎 ?
### 不同指標評比結果相似嗎 ?

