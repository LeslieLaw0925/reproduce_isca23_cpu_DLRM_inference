result_dir=/root/nfs/isca23_dlrm/reproduce_isca23_cpu_DLRM_inference/scripts/fig15/
program_path=/root/nfs/isca23_dlrm/reproduce_isca23_cpu_DLRM_inference/scripts/fig15/24core/normal_run_24c.sh
vtune -collect memory-access -result-dir $result_dir -- $program_path