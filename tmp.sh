res=$(ls results | grep -o "[0-9]*")
for i in $res; do
	set=$(find "results/$i/" | grep "results/[0-9]*/.*.png")
	k=1
	for j in $set; do
		mv $j "results/$i$k"
		k=$((k+1))
	done
	rmdir "results/$i"
done