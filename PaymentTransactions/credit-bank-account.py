import os, sys
import imp

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
constants = imp.load_source('modulename', 'constants.py')
from decimal import *
from authorizenet.apicontractsv1 import bankAccountType, accountTypeEnum

def credit_bank_account():
	merchantAuth = apicontractsv1.merchantAuthenticationType()
	merchantAuth.name = constants.apiLoginId
	merchantAuth.transactionKey = constants.transactionKey


	payment = apicontractsv1.paymentType()

	bankAccountType = apicontractsv1.bankAccountType()
	accountType = apicontractsv1.bankAccountTypeEnum
	bankAccountType.accountType = accountType.checking
	bankAccountType.routingNumber = "125000024"
	bankAccountType.accountNumber = "12345678"
	bankAccountType.nameOnAccount = "John Doe"

	transactionrequest = apicontractsv1.transactionRequestType()
	transactionrequest.transactionType = "refundTransaction"
	transactionrequest.amount = Decimal ('2.55')
	transactionrequest.payment = payment
	transactionrequest.payment.bankAccount = bankAccountType


	createtransactionrequest = apicontractsv1.createTransactionRequest()
	createtransactionrequest.merchantAuthentication = merchantAuth
	createtransactionrequest.refId = "MerchantID-0001"

	createtransactionrequest.transactionRequest = transactionrequest
	createtransactioncontroller = createTransactionController(createtransactionrequest)
	createtransactioncontroller.execute()

	response = createtransactioncontroller.getresponse()

	if response is not None:
		if response.messages.resultCode == "Ok":
			if response.transactionResponse.responseCode == 1:
				print ('Successfully created transaction with Transaction ID: %s' % response.transactionResponse.transId);
				print ('Description: %s' % response.transactionResponse.messages.message[0].description);
			else:
				print ('Failed Transaction.');
				if hasattr(response.transactionResponse, 'errors') == True:
					print ('Error Code:  %s' % str(response.transactionResponse.errors.error[0].errorCode));
					print ('Error message: %s' % response.transactionResponse.errors.error[0].errorText);
		else:
			print ('Failed Transaction.');
			if hasattr(response, 'transactionResponse') == True and hasattr(response.transactionResponse, 'errors') == True:
				print ('Error Code: %s' % str(response.transactionResponse.errors.error[0].errorCode));
				print ('Error message: %s' % response.transactionResponse.errors.error[0].errorText);
			else:
				print ('Error Code: %s' % response.messages.message[0]['code'].text);
				print ('Error message: %s' % response.messages.message[0]['text'].text);
	else:
		print ('Null Response.');

	return response

if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
	credit_bank_account()
