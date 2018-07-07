import os
import base64
import random
import logging
import logging.handlers
import peewee
from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor, db

app = Flask(__name__)
app.debug=True
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    
@app.route('/create', methods=['GET', 'POST'])
def create():
        if request.method == 'POST':
            donorName =  request.form['donor'] 
            donorDonation = request.form['donation']
            try:
                selectedDonor = Donor.create(name=donorName)
            except peewee.IntegrityError:
                selectedDonor = Donor.get(Donor.name == donorName)
            Donation(donor=selectedDonor, value=donorDonation).save()
            donations = Donation.select()
            return render_template('donations.jinja2', donations=donations)
        else:
            return render_template('create.jinja2')


if __name__ == "__main__":
    # create()
    port = int(os.environ.get("PORT", 6738))
    app.run(host='localhost', port=port, debug=True)

