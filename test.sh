# run test.sh file in facex-train-attributes dir


#step1: get det and landmark json file by api
imgOriginalDir=examples/original_img/      #TODO   you need to put your test image into this file, do not need to change
jsonOutDir=examples/landmark_det_result/
python script/landmark_det.py \
        --src ${imgOriginalDir} \
        --rst ${jsonOutDir}

#step2: generate align cpp file and align image 
alignImgDir=examples/align/
clang++ -std=c++11 script/align.cpp -ljson `pkg-config --cflags --libs opencv` -o align.out
./align.out ${jsonOutDir} ${imgOriginalDir} ${alignImgDir}


#step3: generate result
model_def=model/deploy.prototxt
model_weights=model/face_attr_iter_48015.caffemodel
saveImgDir=examples/result/

python script/prediction.py \
        --model_def ${model_def} \
        --model_weights ${model_weights} \
        --jsonfileDir ${jsonOutDir} \
        --alignImgDir ${alignImgDir} \
        --originalImgDir ${imgOriginalDir} \
        --saveImgDir ${saveImgDir} 

