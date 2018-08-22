#step1:
cd setup
tar –xvf scons-2.1.0.tar
cd scons-2.1.0
python setup.py install

#step2:
cd ..
tar -zvxf jsoncpp-src-0.5.0.tar.gz
cd jsoncpp-src-0.5.0
scons platform=linux-gcc

#step3:
# /jsoncpp-src-0.5.0/include/目录下的json文件夹拷贝到/usr/include/
cp -r include/json /usr/include/

#将jsoncpp-src-0.5.0/libs/linux-gcc-4.9.1/目录下的libjson_linux-gcc-4.9.1_libmt.a 拷贝到/usr/local/lib/下，并为了方便使用，将其重命名为libjson.a
cp libs/linux-gcc-5.4.0/libjson_linux-gcc-5.4.0_libmt.a /usr/local/lib/libjson.a