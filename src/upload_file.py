import argparse
import boto3
s3 = boto3.client("s3")

def UploadFile(args):
    """
    Upload one file from Local to S3 bucket.

    Args:
       args.input_file_path(str): local file path of the file to be uploaded
       args.bucket_name(str): S3 bucket name 
       args.output_file_path(str): output file path of uploaded file

    """
    s3.upload_file(args.input_file_path,args.bucket_name,args.output_file_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to S3 Bucket")

    # add argument input_file_path, bucket_name, output_file_path
    parser.add_argument("--input_file_path", help="local file path of uploaded file")
    parser.add_argument("--bucket_name", help="S3 bucket name")
    parser.add_argument("--output_file_path", help="output file path of uploaded file")

    args = parser.parse_args()
    UploadFile(args)