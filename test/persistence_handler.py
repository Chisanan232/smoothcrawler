from abc import ABCMeta, abstractmethod



class BaseFilePersistenceTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_save_procedure(self):
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

    def test_save_procedure(self):
        pass


    def test_split_saving_file(self):
        pass


    def test_save_as_csv(self):
        pass


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
        pass


    def test_all_threads_one_file(self):
        pass


    def test_one_thread_one_file_and_compress_to_one_file(self):
        pass


