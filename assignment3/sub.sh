time_stamp=$(date +%d-%T)
time_stamp="ok${time_stamp}"
mkdir -p "${time_stamp}"

cp ./t1v2.py ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T1.py
echo "Made A3T1 file"
cp ./t2.py ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T2.py
echo "Made A3T2 file"


dos2unix < ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T1.py | cmp - ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T1.py
dos2unix < ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T2.py | cmp - ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T2.py

dos2unix ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T1.py
dos2unix ./"${time_stamp}"/BD_0051_0157_0655_1956_A3T2.py

echo "dos2unix checks done"
