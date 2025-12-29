## Flight Delay Prediction (Machine Learning at Scale)

I would like to thank my teammates for their strong collaboration throughout the project, and our instructor Vinicio de Sola for the thoughtful and constructive feedback.

### Project Summary

Flight delays impose significant costs on travelers in terms of time, financial loss, and logistical coordination. To address this challenge, we developed a traveler-facing predictive engine that provides flight-specific delay estimates up to two hours before departure. Delays are defined as departures occurring 15 minutes or more after the scheduled time, and the task is framed as a regression problem to generate granular delay estimates (in minutes).

We used 30GB of preprocessed dataset for training and evaluated three model families with a walk-forward time-series cross-validation framework: a linear regression baseline, a Multi-Layer Perceptron (MLP) with embeddings for high-cardinality features, and Gradient-Boosted Trees (XGBoost). While linear regression and MLP produced reasonable estimates, both struggled with the highly skewed and zero-inflated delay distribution. To address this, we developed a two-stage XGBoost architecture, consisting of a classifier to estimate delay probability followed by a regressor to predict delay magnitude, paired with a joint evaluation strategy to better penalize large errors.

### My Contributions

In the early stages, I conducted exploratory data analysis and built data processing pipelines informed by the results. 

In later stages, I engineered three centrality-based graph features to capture airport connectivity and congestion. I led and executed 12 XGBoost experiments, exploring hyperparameter configurations, loss functions, model architectures, and sampling strategies. Guided by detailed error analysis, I then designed and implemented the final two-stage XGBoost framework, which significantly improved predictive accuracy and robustness to large delays.


### Final Model Results and Error Analysis

After two MLP experiments and twelve XGBoost-based experiments, our final two-stage model achieved an MAE of 8.46 minutes on the training set and 9.51 minutes on the test set, representing an approximately 35% improvement over the linear baseline and the best overall result.

### Key Takeaways
* Two-stage modeling improves robustness: While RMSE gains were modest, separating delay probability from delay magnitude substantially reduced MAE and improved performance on large delays.
* Extreme delays dominate error: The majority of prediction errors stem from rare, long-delay events, highlighting the importance of tail-aware modeling strategies.
* Evaluation choice shapes conclusions: MAE provided a more informative signal than RMSE for traveler-facing delay predictions, where large outliers are less frequent but more impactful.
* Error analysis drives architecture decisions: Detailed residual analysis directly motivated the shift from single-stage to two-stage modeling and informed future modeling directions.

### Future Work
Several extensions could further improve performance, including:
* Introducing multi-class delay classification prior to regression
* Using separate hyperparameter sets for the classifier and regressor
* Jointly optimizing models with a weighted evaluation metric combining F1 score and MAE
* Applying clustering within each training fold and fitting specialized regression models based on cluster-level delay characteristics

### Tech Stack
* Programming & Data Processing: Python, Pandas, NumPy, PySpark
* Machine Learning: XGBoost, scikit-learn, PyTorch
* Modeling Techniques: Gradient-Boosted Trees, Multi-Layer Perceptrons, Two-Stage Classification–Regression Pipelines
* Feature Engineering: Temporal features, weather-derived variables, historical flight statistics, graph-based network features
