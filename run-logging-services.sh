if [ "$#" -eq 0 ]; then
    num_instances=3
fi

if [ "$#" -eq 1 ]; then
    num_instances=$1
fi

if [ "$#" -gt 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: $0 <number_of_services=3>"
    exit 1
fi

save_file="configs/ports/logging_services.txt"

rm -f $save_file

export PYTHONPATH=.

echo "Starting $num_instances instances of the Logging Service..."
for ((i=0; i<$num_instances; i++)); do
    port=$((42020 + $i))
    python3 loggingService/logging_controller.py --port $port &
    echo $port >> $save_file
done

echo "Started $num_instances instances of the Logging Service."
