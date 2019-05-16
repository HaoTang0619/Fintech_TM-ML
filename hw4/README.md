# HW4: ETF評比績效理論實作 :

### Demo

* 週資料分析組

![image](https://github.com/b05902109/Fintech_TM-ML/blob/master/hw4/week_rank.PNG)

* 月資料分析組 

![image](https://github.com/b05902109/Fintech_TM-ML/blob/master/hw4/month_rank.PNG)

---
### 資料欄位說明

#### 1. ASSR_week_b2_rank (ASSR_month_b2_rank) ;  ASSR_week_b1_rank (ASSR_month_b1_rank)
    · Both calculated by the formula (20) in Portfolio performance evaluation with generalized Sharpe ratios: Beyond the mean and variance (2009)
    · b2 represents investors with logarithmic utility (closer to the real financial market)
    · b1 represents investors with CARA utility

<br>    

#### 2. Sharpe_Omega_week_rank (Sharpe_Omega_month_rank)
    · Calculated by the formula (8) in Omega performance measure and portfolio insurance (2011)

<br>

#### 3. Riskiness_week_uniform_rank (Riskiness_month_uniform_rank) ; Riskiness_week_fitpdf_rank (Riskiness_month_fitpdf_rank)
    · Both calculated by the formula in A global index of riskiness (2013) P.494 Q(g)
    · uniform means using uniform distribution to calculate the expected value
    · fitpdf means using ETF's own probability density function to calculate the expected value

---

### 週資料或月結果評比相似嗎 ?
    · 相似，但排名些微不同。
    · 其中ASSR的周資料與月資料結果評比最為相似
    · Sharpe Omega最不相似(可能因樣本數太小，算出的期望值有誤差而導致)
### 不同指標評比結果相似嗎 ?
    · 部分相似，部分ETF差距很大
    · 因為每一種考慮到的層面不同，因應不同的投資者可能適用不同的方法。
    · 舉例來說： CARA utility的投資者可能就適合使用第二種評比方法(ASSR_week_b1_rank 或 ASSR_month_b1_rank)

