import argparse
import boto3
s3 = boto3.client("s3")


def DownloadFile(args):
	"""
    Download one file from S3 bucket to Local.

    Args:
       args.bucket_name(str): S3 bucket name 
       args.path_of_object_to_download(str): path of the object to download
       args.output_file_path(str): output file path of uploaded file

    """
    s3.download_file(args.bucket_name,args.path_of_object_to_download,args.output_file_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to S3 Bucket")

    # add argument input_file_path, bucket_name, output_file_path
    parser.add_argument("--path_of_object_to_download", help="path of the object to download")
    parser.add_argument("--bucket_name", help="s3 bucket name where you want to download files from")
    parser.add_argument("--output_file_path", help="path to save the downloaded file")

    args = parser.parse_args()
    DownloadFile(args)