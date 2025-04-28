import os
import uuid
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

class S3Service:
    def __init__(self):
        required_env_vars = {
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'AWS_REGION': os.getenv('AWS_DEFAULT_REGION'),
            'AWS_S3_BUCKET': os.getenv('S3_BUCKET_NAME')
        }
        
        missing_vars = [var for var, value in required_env_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Variáveis de ambiente do S3 não configuradas: {', '.join(missing_vars)}")

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=required_env_vars['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=required_env_vars['AWS_SECRET_ACCESS_KEY'],
            region_name=required_env_vars['AWS_REGION'],
            endpoint_url=os.getenv('S3_ENDPOINT_URL')
        )
        self.bucket_name = required_env_vars['AWS_S3_BUCKET']
        self.MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB em bytes
    
    def _gerar_nome_arquivo(self, filename):
        """Gera um nome único para o arquivo"""
        ext = filename.rsplit('.', 1)[1].lower()
        return f"{uuid.uuid4()}.{ext}"
    
    def _validar_arquivo(self, file):
        """Valida se o arquivo é uma imagem permitida"""
        if not file:
            raise ValueError("Nenhum arquivo enviado")
        
        filename = secure_filename(file.filename)
        if not filename:
            raise ValueError("Nome de arquivo inválido")
        
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"Arquivo muito grande. Tamanho máximo permitido é {self.MAX_FILE_SIZE / (1024 * 1024)}MB")
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            raise ValueError("Formato de arquivo não permitido. Use apenas JPG, JPEG ou PNG")
        
        return filename
    
    def upload_file(self, file, folder='produtos'):
        """
        Upload de arquivo para o S3
        :param file: Arquivo a ser enviado
        :param folder: Pasta onde o arquivo será armazenado
        :return: URL do arquivo no S3
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(file.filename)
            unique_filename = f"{timestamp}_{filename}"
            s3_key = f"{folder}/{unique_filename}"

            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ContentType': file.content_type}
            )

            url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            return url

        except ClientError as e:
            print(f"Erro ao fazer upload para o S3: {e}")
            raise

    def delete_file(self, url):
        """
        Deleta um arquivo do S3
        :param url: URL do arquivo no S3
        """
        try:
            key = url.split(f"{self.bucket_name}.s3.amazonaws.com/")[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
        except ClientError as e:
            print(f"Erro ao deletar arquivo do S3: {e}")
            raise
    
    def upload_imagem(self, file):
        """Upload de imagem para o S3"""
        try:
            filename = self._validar_arquivo(file)
            s3_filename = self._gerar_nome_arquivo(filename)
            
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_filename,
                ExtraArgs={'ContentType': f'image/{filename.rsplit(".", 1)[1].lower()}'}
            )
            
            return s3_filename
        except ClientError as e:
            raise ValueError(f"Erro ao fazer upload da imagem: {str(e)}")
    
    def get_url_imagem(self, filename):
        """Retorna a URL pública da imagem"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': filename
                },
                ExpiresIn=3600
            )
            return url
        except ClientError as e:
            raise ValueError(f"Erro ao gerar URL da imagem: {str(e)}")
        
    def download_imagem(self, filename):
        """Faz o download de uma imagem do S3"""
        try:
            temp_dir = 'temp'
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                
            local_path = os.path.join(temp_dir, filename)
            
            self.s3_client.download_file(
                Bucket=self.bucket_name,
                Key=filename,
                Filename=local_path
            )
            
            return local_path
        except ClientError as e:
            raise ValueError(f"Erro ao fazer download da imagem: {str(e)}")

    def deletar_imagem(self, filename):
        """Deleta uma imagem do S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=filename
            )
        except ClientError as e:
            raise ValueError(f"Erro ao deletar imagem: {str(e)}") 