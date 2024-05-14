if [ "$#" -eq 0 ]; then
    num_instances=1
fi

if [ "$#" -eq 1 ]; then
    num_instances=$1
fi

if [ "$#" -gt 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: $0 <number_of_services=2>"
    exit 1
fi

export PYTHONPATH=.

for ((i=0; i<=$num_instances; i++)); do
    port=$((42000 + $i))
    export PORT=$port
    python3 facadeService/facade_controller.py --port $port &
done

echo "Started $num_instances receivedinstances of the Facade Service."
