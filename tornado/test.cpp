#include <assert.h>
#include <string.h>
#include <leveldb/db.h>
#include <iostream>
#include <fstream>
using namespace std;

int main(){
    leveldb::DB* db;
    leveldb::Options options;
    // options.create_if_missing = true;
    // options.error_if_exists = true;
    leveldb::Status status = leveldb::DB::Open(options,"/opt/Storage/Disk_02/DATA/volume_table_0", &db);
   // leveldb::Status status = leveldb::DB::Open(options,"/opt/Storage/Disk_00/DATA/master_table_default", &db);
    //leveldb::Status status = leveldb::DB::Open(options,"/tmp/testdb/", &db);
    assert(status.ok());

    // write key1,value1
    std::string key="0000000000";
    std::string value = "";
    status = db->Get(leveldb::ReadOptions(), key, &value);
    assert(status.ok());
    ofstream outFile;
    
    outFile.open("/dev/shm/sample.txt");
    outFile <<value;
    outFile.close();

   // fout.open("./md5.txt");
   // fout << value<<"\n";
   // fout << flush;fout.close();
    // status = db->Get(leveldb::ReadOptions(), key, &value);
   // assert(status.ok());
    // std::cout<<"passwd = "<<value<<std::endl;

    leveldb::Iterator* it = db->NewIterator(leveldb::ReadOptions());
    for (it->SeekToFirst(); it->Valid(); it->Next()) {
      std::cout << it->key().ToString() << ": "  << std::endl;
    }
    assert(it->status().ok());  // Check for any errors found during the scan
    delete it;

    // move the value under key to key2
    // status = db->Delete(leveldb::WriteOptions(), key);
 
   // if(status.ok()) std::cerr<<key<<"  "<<status.ToString()<<std::endl;
   // else std::cout<<"key3 not found"<<std::endl;
 
    delete db;
    
    return 0;
}
