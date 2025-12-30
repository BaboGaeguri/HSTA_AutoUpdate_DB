# AWS 배포 가이드

## 사전 준비

### 1. AWS 계정 및 IAM 설정

1. AWS Console에서 IAM > Users > 사용자 선택
2. Permissions 탭 > Add permissions > Attach policies directly
3. Create policy 클릭
4. JSON 탭 선택 후 `iam-policy.json` 내용 복사/붙여넣기
5. 정책 이름: `HSTA-Deploy-Policy`로 저장
6. 사용자에게 정책 연결

### 2. EC2 키 페어 생성

1. AWS Console > EC2 > Key Pairs
2. Create key pair
3. 이름: `hsta-key` (또는 원하는 이름)
4. `.pem` 파일 다운로드 및 안전한 곳에 보관

### 3. 환경 변수 설정

#### `.env` 파일 생성
```bash
cp .env.example .env
```

`.env` 파일 내용:
```
AWS_REGION=ap-northeast-2
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_ACCOUNT_ID=YOUR_ACCOUNT_ID
EC2_KEY_PAIR_NAME=hsta-key
ECR_REPOSITORY_NAME=hsta-app
FLASK_ENV=production
FLASK_APP=app.py
```

#### `terraform.tfvars` 파일 생성
```bash
cp terraform.tfvars.example terraform.tfvars
```

`terraform.tfvars` 파일 내용:
```hcl
aws_region    = "ap-northeast-2"
instance_type = "t3.micro"
ami_id        = "ami-0c9c942bd7bf113a2"
key_pair_name = "hsta-key"
```

## Terraform으로 인프라 구축

### 1. Terraform 초기화
```bash
terraform init
```

### 2. 인프라 계획 확인
```bash
terraform plan
```

### 3. 인프라 생성
```bash
terraform apply
```

확인 메시지가 나오면 `yes` 입력

### 4. 출력 정보 확인
```bash
terraform output
```

다음 정보를 메모:
- `ecr_repository_url`: ECR 리포지토리 URL
- `ec2_public_ip`: EC2 공용 IP 주소

## GitHub Actions 설정

### GitHub Secrets 추가

Repository > Settings > Secrets and variables > Actions > New repository secret

다음 secrets 추가:

1. `AWS_ACCESS_KEY_ID`: AWS Access Key
2. `AWS_SECRET_ACCESS_KEY`: AWS Secret Key
3. `EC2_HOST`: EC2 공용 IP (terraform output에서 확인)
4. `EC2_SSH_KEY`: EC2 키 페어 내용 (.pem 파일 전체 내용)

### EC2_SSH_KEY 설정 방법
```bash
# Windows (PowerShell)
Get-Content hsta-key.pem | Set-Clipboard

# 또는 파일 내용을 텍스트 에디터로 열어서 복사
```

복사한 내용을 GitHub Secret에 붙여넣기

## 배포

### 자동 배포 (권장)
main 브랜치에 push하면 자동으로 배포됩니다:
```bash
git add .
git commit -m "Deploy to AWS"
git push origin main
```

### 수동 배포 (선택)
```bash
# ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com

# Docker 이미지 빌드
docker build -t hsta-app .

# 이미지 태깅
docker tag hsta-app:latest YOUR_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/hsta-app:latest

# ECR에 푸시
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/hsta-app:latest

# EC2에 SSH 접속
ssh -i hsta-key.pem ec2-user@EC2_PUBLIC_IP

# EC2에서 실행
docker pull YOUR_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/hsta-app:latest
docker run -d --name hsta-app -p 80:5000 --restart unless-stopped YOUR_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/hsta-app:latest
```

## 접속 확인

웹 브라우저에서 접속:
```
http://EC2_PUBLIC_IP
```

## 인프라 삭제

사용을 중지하려면:
```bash
terraform destroy
```

## 트러블슈팅

### ECR 로그인 실패
- AWS credentials 확인
- IAM 정책이 올바르게 설정되었는지 확인

### GitHub Actions 실패
- GitHub Secrets가 모두 설정되었는지 확인
- EC2 보안 그룹에서 22번 포트(SSH)가 열려있는지 확인

### EC2 접속 실패
- 보안 그룹 인바운드 규칙 확인
- 키 페어가 올바른지 확인
- EC2 인스턴스가 실행 중인지 확인

### 웹 접속 실패
- EC2에서 Docker 컨테이너가 실행 중인지 확인: `docker ps`
- 컨테이너 로그 확인: `docker logs hsta-app`
- 보안 그룹에서 80번 포트가 열려있는지 확인
