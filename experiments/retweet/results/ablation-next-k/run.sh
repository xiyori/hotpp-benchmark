for method in next_k rmtpp_k; do
    for k in 1 2 3 4 5 8; do
        python3 -m esp_horizon.train --config-dir configs --config-name $method ++max_predictions=$k ++name=${method}_$k '~metric.otd_steps'
    done

    for k in 12 16 24; do
        python3 -m esp_horizon.train --config-dir configs --config-name $method ++max_predictions=$k ++name=${method}_$k
    done
done
