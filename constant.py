from flask import Flask, render_template, json, request, redirect, session, url_for, flash
import pymysql

def conn():
    return pymysql.connect(host='localhost',
                    user='root',
                    password='123456',
                    db='am_db',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

