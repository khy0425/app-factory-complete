#!/usr/bin/env python3
import requests
import json

def create_github_repository(name, description="Chad workout app"):
    github_token = "your_github_token_here"

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": name,
        "description": description,
        "private": False,
        "auto_init": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        repo_data = response.json()
        print(f"✅ 저장소 생성 성공: {repo_data['clone_url']}")
        return repo_data['clone_url']
    else:
        print(f"❌ 저장소 생성 실패: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    repo_url = create_github_repository("squat-master", "Chad-themed squat challenge app")
    if repo_url:
        print(f"GitHub 저장소: {repo_url}")