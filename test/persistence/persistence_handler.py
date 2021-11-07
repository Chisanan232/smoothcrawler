from smoothcrawler.persistence.file import (
    SavingStrategy,
    SavingMediator,
    FileSaver, File, CSVFormatter, ArchiverSaver, ZIPArchiver)

from abc import ABCMeta, abstractmethod
from typing import List, Dict
from pathlib import Path
import threading
import csv
import os

Test_CSV_File_Path: str = str(Path("./for_testing.csv"))
Test_XLSX_File_Path: str = "for_testing.xlsx"
Test_JSON_File_Path: str = "for_testing.json"
Test_Mode: str = "a+"

Test_Data_List: List = [
    ['0108-01-02 00:00:00', 32900482.0, 7276419230.0, 226.5, 226.5, 219.0, 219.5, 12329.0],
    ['0108-01-03 00:00:00', 34615620.0, 7459051790.0, 214.0, 218.0, 214.0, 215.5, 14549.0],
    ['0108-01-04 00:00:00', 67043521.0, 13987136785.0, 211.5, 211.5, 206.5, 208.0, 28786.0]
]

Test_JSON_Data: Dict = {"data": [
    ['0108-01-02 00:00:00', 32900482.0, 7276419230.0, 226.5, 226.5, 219.0, 219.5, 12329.0],
    ['0108-01-03 00:00:00', 34615620.0, 7459051790.0, 214.0, 218.0, 214.0, 215.5, 14549.0],
    ['0108-01-04 00:00:00', 67043521.0, 13987136785.0, 211.5, 211.5, 206.5, 208.0, 28786.0]
]}

Run_Open_Process_Flag: bool = False
Run_Write_Process_Flag: bool = False
Run_Close_Process_Flag: bool = False
Run_Procedure_List: List[str] = []
Run_Result_Data_List = []

Thread_Number = 3
Thread_Counter = 0
Thread_Lock = threading.Lock()


class _TestFile(File):

    def open(self) -> None:
        global Run_Open_Process_Flag, Run_Procedure_List
        Run_Open_Process_Flag = True
        Run_Procedure_List.append("open")
        print("Running 'open' process to initial file object.")


    def write(self, data: List[list]) -> None:
        global Run_Write_Process_Flag, Run_Procedure_List
        Run_Write_Process_Flag = True
        Run_Procedure_List.append("write")
        print("Running 'write' process to save data into target file object.")


    def close(self) -> None:
        global Run_Close_Process_Flag, Run_Procedure_List
        Run_Close_Process_Flag = True
        Run_Procedure_List.append("close")
        print("Running 'close' process to finish file object.")


    def stream(self, data: List[list]) -> str:
        pass



class _TestMultiThread(threading.Thread):

    def __init__(self, fs: FileSaver, ars: ArchiverSaver = None):
        super().__init__()
        self.fs = fs
        self.ars = ars

    def run(self) -> None:
        with Thread_Lock:
            global Thread_Counter
            data = Test_Data_List[Thread_Counter]
            print(f"Get data: {data} - {self.getName()}")
            final_data = self.fs.save(file=f"for_testing_{Thread_Counter}.csv", mode="a+", data=[data])
            print(f"Final Data: {final_data}")
            print(f"[DEBUG] Final Data file_path: {final_data.file_path}")
            print(f"[DEBUG] Final Data data: {final_data.data}")
            if self.fs.has_data():
                Run_Result_Data_List.append(final_data)
            Thread_Counter += 1



class _TestMainThread:

    __File_Saver = None
    __Archiver_Saver = None

    def __init__(self, strategy: SavingStrategy):
        test_mediator = SavingMediator()
        self.__File_Saver = FileSaver(file=CSVFormatter())
        self.__File_Saver.register(mediator=test_mediator, strategy=strategy)

        self.__Archiver_Saver = ArchiverSaver(archiver=ZIPArchiver())
        self.__Archiver_Saver.register(mediator=test_mediator, strategy=strategy)


    def process(self):
        thread_list = [_TestMultiThread(fs=self.__File_Saver, ars=self.__Archiver_Saver) for _ in range(Thread_Number)]
        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        print(f"[DEBUG] Run_Result_Data_List: {Run_Result_Data_List}")
        self.__File_Saver.save(file=f"for_testing_all.csv", mode="a+", data=Run_Result_Data_List)
        self.__Archiver_Saver.compress(file=f"for_testing.zip", mode="a", data=Run_Result_Data_List)



class BaseFilePersistenceTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_saving_procedure(self):
        pass


    @abstractmethod
    def test_saving_stream_procedure(self):
        pass


    @abstractmethod
    def test_saving_procedure_with_mediator(self):
        pass


    @abstractmethod
    def test_split_saving_file(self):
        pass


    @abstractmethod
    def test_save_as_csv(self):
        pass


    @abstractmethod
    def test_save_as_xlsx(self):
        pass


    @abstractmethod
    def test_compress_procedure(self):
        pass


    @abstractmethod
    def test_compress_as_zip(self):
        pass


    @abstractmethod
    def test_compress_as_tar(self):
        pass


    @abstractmethod
    def test_save_as_csv_and_compress_as_zip(self):
        pass


    @abstractmethod
    def test_save_as_csv_and_compress_as_tar(self):
        pass


    @abstractmethod
    def test_save_as_xlsx_and_compress_as_zip(self):
        pass


    @abstractmethod
    def test_save_as_xlsx_and_compress_as_tar(self):
        pass


    @abstractmethod
    def test_one_thread_one_file(self):
        pass


    @abstractmethod
    def test_all_threads_one_file(self):
        pass


    @abstractmethod
    def test_one_thread_one_file_and_compress_to_one_file(self):
        pass



class TestFilePersistence(BaseFilePersistenceTestSpec):

    def test_saving_procedure(self):

        class TestErrorFormatter:
            pass

        # Test for invalid value
        try:
            fs = FileSaver(file=TestErrorFormatter())
        except TypeError as e:
            assert type(e) is TypeError, "It should raise exception 'TypeError' if the option value is invalid."
        except Exception as e:
            assert False, "Occur something unexpected error."

        # Test for CSV
        fs = FileSaver(file=_TestFile())
        fs.save(file="no.no", mode="yee", encoding="UTF-8", data=Test_Data_List)
        assert Run_Open_Process_Flag is True, "It should experience 'open' process."
        assert Run_Write_Process_Flag is True, "It should experience 'write' process."
        assert Run_Close_Process_Flag is True, "It should experience 'close' process."
        assert Run_Procedure_List[0] == "open", "It should run 'open' process first."
        assert Run_Procedure_List[1] == "write", "It should run 'write' process second."
        assert Run_Procedure_List[2] == "close", "It should run 'close' process finally."

        TestFilePersistence._init_flag()


    @staticmethod
    def _init_flag():
        global Run_Open_Process_Flag, Run_Write_Process_Flag, Run_Close_Process_Flag
        Run_Open_Process_Flag = False
        Run_Write_Process_Flag = False
        Run_Close_Process_Flag = False


    def test_saving_stream_procedure(self):
        pass


    def test_saving_procedure_with_mediator(self):
        fs = FileSaver(file=_TestFile())
        mediator = SavingMediator()
        mediator.worker_id = ""
        fs.register(mediator=mediator, strategy=SavingStrategy.ALL_THREADS_ONE_FILE)


    def test_split_saving_file(self):
        pass


    def test_save_as_csv(self):
        fs = FileSaver(file=CSVFormatter())
        fs.save(file=Test_CSV_File_Path, mode=Test_Mode, encoding="UTF-8", data=Test_Data_List)
        exist_csv_file = os.path.exists(Test_CSV_File_Path)
        assert exist_csv_file is True, "It should exist a .csv file."
        with open(Test_CSV_File_Path, "r") as csv_file:
            data = csv.reader(csv_file)
            for index, d in enumerate(data):
                print(f"Data row: {d}")
                print(f"Test_Data_List[{index}]: {Test_Data_List[index]}")
                for ele_d, ele_o in zip(d, Test_Data_List[index]):
                    assert str(ele_d) == str(ele_o), "Each values in the data row should be the same."

        os.remove(Test_CSV_File_Path)


    def test_save_as_xlsx(self):
        pass


    def test_compress_procedure(self):
        pass


    def test_compress_as_zip(self):
        pass


    def test_compress_as_tar(self):
        pass


    def test_save_as_csv_and_compress_as_zip(self):
        pass


    def test_save_as_csv_and_compress_as_tar(self):
        pass


    def test_save_as_xlsx_and_compress_as_zip(self):
        pass


    def test_save_as_xlsx_and_compress_as_tar(self):
        pass


    def test_one_thread_one_file(self):
        TestFilePersistence._init_thread_counter()

        tmt = _TestMainThread(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
        tmt.process()

        for i in range(Thread_Counter - 1, -1, -1):
            file_name = f"./for_testing_{i}.csv"
            exist_file = os.path.exists(file_name)
            assert exist_file is True, f"It should exist .csv file {file_name}"
            os.remove(file_name)


    def test_all_threads_one_file(self):
        TestFilePersistence._init_thread_counter()

        tmt = _TestMainThread(strategy=SavingStrategy.ALL_THREADS_ONE_FILE)
        tmt.process()

        file_name = f"./for_testing_all.csv"
        exist_file = os.path.exists(file_name)
        assert exist_file is True, f"It should exist .csv file {file_name}"
        os.remove(file_name)


    def test_one_thread_one_file_and_compress_to_one_file(self):
        TestFilePersistence._init_thread_counter()

        tmt = _TestMainThread(strategy=SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL)
        tmt.process()

        file_name = f"./for_testing.zip"
        exist_file = os.path.exists(file_name)
        assert exist_file is True, f"It should exist .zip file {file_name}"
        # assert False is True, "Just look log message and file content."
        os.remove(file_name)


    @staticmethod
    def _init_thread_counter():
        global Thread_Counter, Run_Result_Data_List
        Thread_Counter = 0
        Run_Result_Data_List = []


