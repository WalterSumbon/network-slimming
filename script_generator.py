name_list=[]

def cmd_b(depth,epochs,lr):
    dirname = "results/depth-%d/baseline"%depth
    name = "t-%d-b.sh"%depth
    ss="""#!/bin/bash
#SBATCH -N 1 -n 8 -p GPU-V100 --gres=gpu:v100:1
module load cuda/10.2.89
module load anaconda3
module load python/3.8.1
module load cudnn/7.6.5/cuda/9.2
module load openmpi/4.0.3/gcc/9.3.0
source activate ns

dataset=cifar10
arch=resnet
depth=%d
prune_code="resprune.py"
epochs=%d
lr=%g
echo baseline
dirname=%s

mkdir -p ${dirname}
echo ${dataset}
echo ${s}
echo ${arch}
echo ${depth}
echo ${prune_code}
echo ${epochs}
echo ${lr}
echo ${dirname}

startTime=`date +%%Y%%m%%d-%%H:%%M`
startTime_s=`date +%%s`

python main.py --dataset ${dataset} --arch ${arch} --depth ${depth} --save ./${dirname} --epochs ${epochs} --lr ${lr} 

endTime=`date +%%Y%%m%%d-%%H:%%M`
endTime_s=`date +%%s`
sumTime=$[ $endTime_s - $startTime_s ]
echo "$startTime ---> $endTime" "Total:$sumTime sec"
"""%(depth,epochs,lr,dirname)
    with open(name,'w') as f:
        f.write(ss)
    name_list.append(name)

def cmd_sp(s,depth,epochs,lr):
    dirname = "results/depth-%d/sp"%depth
    name = "t-%d-sp.sh"%depth
    ss="""#!/bin/bash
#SBATCH -N 1 -n 8 -p GPU-V100 --gres=gpu:v100:1
module load cuda/10.2.89
module load anaconda3
module load python/3.8.1
module load cudnn/7.6.5/cuda/9.2
module load openmpi/4.0.3/gcc/9.3.0
source activate ns

dataset=cifar10
s=%f
arch=resnet
depth=%d
epochs=%d
lr=%g
dirname=%s

mkdir -p ${dirname}

echo ${dataset}
echo ${s}
echo ${arch}
echo ${depth}
echo ${epochs}
echo ${lr}
echo ${dirname}

startTime=`date +%%Y%%m%%d-%%H:%%M`
startTime_s=`date +%%s`

python main.py --dataset ${dataset} --arch ${arch} --depth ${depth} --save ./${dirname} --epochs ${epochs} --lr ${lr} -sr --s ${s}

endTime=`date +%%Y%%m%%d-%%H:%%M`
endTime_s=`date +%%s`
sumTime=$[ $endTime_s - $startTime_s ]
echo "$startTime ---> $endTime" "Total:$sumTime sec"

done
"""%(s,depth,epochs,lr,dirname)
    with open(name,'w') as f:
        f.write(ss)
    name_list.append(name)

def cmd_p(depth):
    
    ss="""#!/bin/bash
#SBATCH -N 1 -n 8 -p GPU-V100 --gres=gpu:v100:1
module load cuda/10.2.89
module load anaconda3
module load python/3.8.1
module load cudnn/7.6.5/cuda/9.2
module load openmpi/4.0.3/gcc/9.3.0
source activate ns

dataset=cifar10
arch=resnet
depth=%d
prune_code="resprune.py"
percents=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
for percent in ${percents[@]}
do
dirname="results/depth-${depth}/percent-${percent}/pruned"

mkdir -p ${dirname}
echo ${dataset}
echo ${arch}
echo ${depth}
echo ${prune_code}
echo ${percent}
echo ${dirname}

startTime=`date +%%Y%%m%%d-%%H:%%M`
startTime_s=`date +%%s`

python ${prune_code} --dataset ${dataset} --depth ${depth} --percent ${percent} --model ./results/depth-${depth}/sp/model_best.pth.tar --save ./${dirname}

endTime=`date +%%Y%%m%%d-%%H:%%M`
endTime_s=`date +%%s`
sumTime=$[ $endTime_s - $startTime_s ]
echo "$startTime ---> $endTime" "Total:$sumTime sec"

done
"""%depth
    with open(f"p-{depth}.sh",'w') as f:
        f.write(ss)


def cmd_ft(depth,epochs,lr,percents):
    ss="""#!/bin/bash
#SBATCH -N 1 -n 8 -p GPU-V100 --gres=gpu:v100:1
module load cuda/10.2.89
module load anaconda3
module load python/3.8.1
module load cudnn/7.6.5/cuda/9.2
module load openmpi/4.0.3/gcc/9.3.0
source activate ns

dataset=cifar10
arch=resnet
depth=%d
epochs=%d
lr=%g
percents=(%s)

for percent in ${percents[@]}
do
dirname="results/depth-${depth}/percent-${percent}/ft" 

mkdir -p ${dirname}
echo ${dataset}
echo ${arch}
echo ${depth}
echo ${percent}
echo ${epochs}
echo ${lr}
echo ${dirname}
echo ft

startTime=`date +%%Y%%m%%d-%%H:%%M`
startTime_s=`date +%%s`

python main.py --refine ./results/depth-${depth}/percent-${percent}/pruned --dataset ${dataset} --arch ${arch} --depth ${depth} --epochs ${epochs} --save ./${dirname} --lr ${lr} 

endTime=`date +%%Y%%m%%d-%%H:%%M`
endTime_s=`date +%%s`
sumTime=$[ $endTime_s - $startTime_s ]
echo "$startTime ---> $endTime" "Total:$sumTime sec"

done
"""%(depth,epochs,lr,' '.join([str(p) for p in percents]))
    percents = '_'.join([str(p) for p in percents])
    with open(f't-{depth}-ft-{percents}.sh','w') as f:
        f.write(ss)

def cmd_fs(depth,epochs,lr,percents):
    ss="""#!/bin/bash
#SBATCH -N 1 -n 8 -p GPU-V100 --gres=gpu:v100:1
module load cuda/10.2.89
module load anaconda3
module load python/3.8.1
module load cudnn/7.6.5/cuda/9.2
module load openmpi/4.0.3/gcc/9.3.0
source activate ns

dataset=cifar10
arch=resnet
depth=%d
epochs=%d
lr=%g
percents=(%s)

for percent in ${percents[@]}
do
dirname="results/depth-${depth}/percent-${percent}/ft" 

mkdir -p ${dirname}
echo ${dataset}
echo ${arch}
echo ${depth}
echo ${percent}
echo ${epochs}
echo ${lr}
echo ${dirname}
echo fs

startTime=`date +%%Y%%m%%d-%%H:%%M`
startTime_s=`date +%%s`

python main.py --refine ./results/depth-${depth}/percent-${percent}/pruned --dataset ${dataset} --arch ${arch} --depth ${depth} --epochs ${epochs} --save ./${dirname} --lr ${lr} -fs

endTime=`date +%%Y%%m%%d-%%H:%%M`
endTime_s=`date +%%s`
sumTime=$[ $endTime_s - $startTime_s ]
echo "$startTime ---> $endTime" "Total:$sumTime sec"

done
"""%(depth,epochs,lr,' '.join([str(p) for p in percents]))
    percents = '_'.join([str(p) for p in percents])
    with open(f't-{depth}-fs-{percents}.sh','w') as f:
        f.write(ss)

#s,depth,epochs,lr,percent=None,fs=False,baseline=False
a=[[0.1,0.2,0.3],[0.4,0.5,0.6],[0.7,0.8,0.9]]
b=[20,56,164]
for d in b:
    cmd_b(d,300,0.1)
    cmd_sp(0.0001,d,300,0.01)
    cmd_p(d)
    for lst in a:
        cmd_fs(d,300,0.1,lst)
        cmd_ft(d,300,0.01,lst)