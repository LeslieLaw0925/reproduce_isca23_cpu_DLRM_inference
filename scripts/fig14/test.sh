for i in $(seq 0 0x1fff); do
  sudo rdmsr $i 2>/dev/null && echo "MSR 0x$(printf "%x" $i) is supported"
done
