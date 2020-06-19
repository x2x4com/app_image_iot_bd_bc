FROM python:3.7-stretch


# 新代码
COPY . /app
# RUN rm -rf /app/.git && rm -rf /app/venv
RUN mkdir /app/staticfiles
# RUN chown -R deploy:deploy /blockscanner
WORKDIR /app

RUN pip3 install pip --upgrade --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple \
 && pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


EXPOSE 8000

# ENTRYPOINT
# ENTRYPOINT ["./app_init.sh"]
CMD ["./start.sh"]