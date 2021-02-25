./configure --prefix=/usr/local/protobuf
make && make install
export PATH=/usr/local/protobuf/bin:$PATH
protoc --version

vim addressbook.proto
protoc --python_out=./ ./addressbook_pb.proto