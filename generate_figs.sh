input_folder=analyze/results
tmp_folder=res_tmp

mkdir $tmp_folder -p
mkdir pictures -p

for file in common.py utils.py; do
    cp $input_folder/$file $tmp_folder/$file
done

for file in by_one_subsidity_level.ipynb by_alpha_build.ipynb by_alpha_subs.ipynb by_energy_factor.ipynb by_energy_price.ipynb by_fuel_price.ipynb by_PHEV_subs.ipynb main_results_by_gov.ipynb;
# for file in main_results_by_gov.ipynb by_energy_price.ipynb by_fuel_price.ipynb by_PHEV_subs.ipynb;
# for file in LiberalIntervals.ipynb intervalsSubs.ipynb intervalsBuild.ipynb intervalsMixed.ipynb;
do
    echo $input_folder/$file
    poetry run python3 -m menage_jupyter -o $tmp_folder/$file --force 1 jupyter2py $input_folder/$file
    poetry run python3 $tmp_folder/$file
done

rm -fr $tmp_folder
