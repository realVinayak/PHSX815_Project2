# PHSX815_Project2

About this project:<br/>
An important goal of doing experiments is to resolve between the test hypothesis and the null 
hypothesis, and false negative rate is a metric to measure how well the hypothesis are separated. 
The hypothesis in consideration can be complex - that is they can have multiple intermediary
distributions before the final value is observed. The goal of this project is to study how the 
false negative rate is affected by the complexity of the model

<br/>
The complexity of the hypothesis is modelled through depth with Gaussian distribution. 
Depth is the number of intermediary distributions which are sampled before final value is 
observed. So, if depth = 3, then there are three intermediary Gaussian distributions and the output from
Gaussian distribution controls the mean and standard deviation of the next one, and thus, model gets
"complex". 

<h2>Code Structure and Components</h2>
1. `utils.py`: Contains three important functions:
<ul>
    <li>
        <h3>get_log_likelihood_ratio(measurement, get_first_prob, get_second_prob)</h3>
        <p>Calculates the log likelihood ratio of a single measurement. Here, get_first_prob and get_second_prob 
        are functions that return probability of measurement under first distribution
        and second distribution
        </p>
    </li>
    <li>
        <h3>
        get_fnr(llr_measurements, lambda_threshold)
        </h3>    
        <p>Iterates through log-likelihood ratios returns the fraction of 
        llr_measurements which have log-likelihood ratio above lambda_threshold.
        This function is used to calculate the false negative rate.
        </p>
    </li>
    <li>
        <h3>get_probability_from_hist(hist_data, hist_bins, sample)</h3>
        <p>Returns the probability of sample by reading the height
           of the histogram (hist_data) for the histogram bin which
           includes the input sample
        </p>
    </li>
</ul>

2. `compound_gaussian.py`: The main generator to simulate the experiment. The file defines 
    all the global variables for the analysis - initial means, number of samples per experiment,
    depth of the model (complexity), percentile limit (alpha). 
 <br/>`generate_measurements(num_meas, depth)`
    is the function that simulates `N_experiments` experiments with `num_meas` measurements in each experiment. 
    Additionally, the `depth` is the number of intermediary Gaussian distributions sampled (more info above).
    To streamline data generation, I call this function with varying `num_meas` and `depth` - defined as parameters
   at top of this file. Note that we get
   a different set of measurements for hypothesis 1 and hypothesis 2 - that is, we will have to do the process twice
   for each hypothesis while keeping `num_meas` and `depth` same, as it is assumed that the only difference between
    the two hypothesis is the initial mean (hyperparameter defined as $\gamma for each hypothesis). The outputs are 
    stored in `./outputs/measurements` as txt file and the filename is calculated as `measurements_{num_meas}_{depth}_hypo_{1 or 2}.txt`.
    <br/> Type `python3 compound_gaussian.py` to generate the samples.
3. `analyze_data.py`: The main file to analyze the measurements from experiments from `compound_gaussian.py`. The main 
    function used in the file is the `analyze_atomic(num_meas, depth)` which analyzes the measurements from the file `measurements_{num_meas}_{depth}_hypo_1.txt` and `measurements_{num_meas}_{depth}_hypo_2.txt`.
    This function returns the false negative rate between the test hypothesis and the null hypothesis, both of which are complex
    hypothesis with number of measurements in an experiment equal to `num_meas` and depth (intermediary Gaussian steps) equal to `depth`. <br/>Additionally, this file generates the log-likelihood ratio's histogram conditioned on the hypothesis, thus depends on `num_meas` and `depth`. The log-likelihood ratio
    histogram for a particular value of `num_meas` and `depth` is stored in `./outputs/histograms/measurements_{num_meas}_depth_{depth}.png`.
    <br/>Further, the file stores the false negative rate for each pair of `num_meas` and `depth` simulated by the generator
    and produces a heat-map. The false negative rate's heatmap is stored in the main directory as `fnr_heatmap.png`. 
4. `./outputs/`: Contains all the important outputs out of the code. `./outputs/` is divided into two
    directories. 
    <ul>
       <li>
        <h3>`./outputs/measurements/`</h3>
        <p>Contains all the measured values generated during the generation process. The file names are 
        determined by the number of measurements per an experiment, the depth (complexity), and whether
        the samples were drawn from test hypothesis or null hypothesis.
        </p>
        </li>
        <li>
        <h3>./outputs/histograms/</h3> 
        <p>Contains all the histograms generated during the analysis process. A histogram is calculated
           for each pair of number of measurements per an experiment and the depth. 
        </p>
        </li>        

    </ul>
5. `file_list_utils.py`: Contains functions to load and write lists to and from txt files simpler. Also supports multidimensional lists.
6. `histogram_utils.py`: File contains `get_histogram_data()` which takes in measurements and number of samples and first generates a histogram using numpy (but doesn't plot it) and then returns a 2-d list of bins and probability at each bin which is used to plot. I had to implement this since MatPlotLib's histogram was slow for 1,000,000+ experiments.