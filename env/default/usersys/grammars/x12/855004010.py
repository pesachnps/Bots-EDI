# X12 855 - Purchase Order Acknowledgment (Version 004010)
# Transaction Set for acknowledging receipt of purchase orders
# Functional Group: PR (Purchase Order Acknowledgment)

from bots.botsconfig import *
from .records004010 import recorddefs

syntax = {
    'version': '00401',  # version of ISA to send
    'functionalgroup': 'PR',  # Purchase Order Acknowledgment
}

structure = [
{ID: 'ST', MIN: 1, MAX: 1, LEVEL: [
    # Beginning Segment for Purchase Order Acknowledgment
    {ID: 'BAK', MIN: 1, MAX: 1},
    
    # Currency - optional
    {ID: 'CUR', MIN: 0, MAX: 1},
    
    # Reference Identification - up to 99999
    {ID: 'REF', MIN: 0, MAX: 99999},
    
    # Administrative Communications Contact - up to 3
    {ID: 'PER', MIN: 0, MAX: 3},
    
    # Tax Reference - up to 99999
    {ID: 'TAX', MIN: 0, MAX: 99999},
    
    # F.O.B. Related Instructions - up to 99999
    {ID: 'FOB', MIN: 0, MAX: 99999},
    
    # Pricing Information - up to 99999
    {ID: 'CTP', MIN: 0, MAX: 99999},
    
    # Periodic Amount - up to 10
    {ID: 'PAM', MIN: 0, MAX: 10},
    
    # Service, Promotion, Allowance, or Charge Information - up to 25
    {ID: 'SAC', MIN: 0, MAX: 25, LEVEL: [
        {ID: 'CUR', MIN: 0, MAX: 1},
    ]},
    
    # Terms of Sale/Deferred Terms of Sale - up to 99999
    {ID: 'ITD', MIN: 0, MAX: 99999},
    
    # Discount Detail - up to 20
    {ID: 'DIS', MIN: 0, MAX: 20},
    
    # Date/Time Reference - up to 10
    {ID: 'DTM', MIN: 0, MAX: 10},
    
    # Product/Item Description - up to 200
    {ID: 'PID', MIN: 0, MAX: 200},
    
    # Measurements - up to 40
    {ID: 'MEA', MIN: 0, MAX: 40},
    
    # Paperwork - up to 25
    {ID: 'PWK', MIN: 0, MAX: 25},
    
    # Marking, Packaging, Loading - up to 200
    {ID: 'PKG', MIN: 0, MAX: 200},
    
    # Carrier Details (Quantity and Weight) - up to 2
    {ID: 'TD1', MIN: 0, MAX: 2},
    
    # Carrier Details (Routing Sequence/Transit Time) - up to 12
    {ID: 'TD5', MIN: 0, MAX: 12},
    
    # Carrier Details (Equipment) - up to 12
    {ID: 'TD3', MIN: 0, MAX: 12},
    
    # Carrier Details (Special Handling, or Hazardous Materials, or Both) - up to 5
    {ID: 'TD4', MIN: 0, MAX: 5},
    
    # Marks and Numbers - up to 10
    {ID: 'MAN', MIN: 0, MAX: 10},
    
    # Tax Information - up to 99999
    {ID: 'TXI', MIN: 0, MAX: 99999},
    
    # Extended Reference Information - up to 1000
    {ID: 'N9', MIN: 0, MAX: 1000, LEVEL: [
        {ID: 'DTM', MIN: 0, MAX: 99999},
        {ID: 'MSG', MIN: 0, MAX: 1000},
        {ID: 'MTX', MIN: 0, MAX: 99999},
    ]},
    
    # Name/Address Loop - up to 200
    {ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
        {ID: 'N2', MIN: 0, MAX: 2},
        {ID: 'N3', MIN: 0, MAX: 2},
        {ID: 'N4', MIN: 0, MAX: 1},
        {ID: 'REF', MIN: 0, MAX: 12},
        {ID: 'PER', MIN: 0, MAX: 3},
        {ID: 'DTM', MIN: 0, MAX: 1},
    ]},
    
    # Code Source Information - up to 99999
    {ID: 'LM', MIN: 0, MAX: 99999, LEVEL: [
        {ID: 'LQ', MIN: 1, MAX: 99999},
    ]},
    
    # Baseline Item Data (Acknowledgment) Loop - up to 100000
    {ID: 'ACK', MIN: 0, MAX: 100000, LEVEL: [
        # Date/Time Reference - up to 10
        {ID: 'DTM', MIN: 0, MAX: 10},
        
        # Product/Item Description - up to 1000
        {ID: 'PID', MIN: 0, MAX: 1000, LEVEL: [
            {ID: 'MEA', MIN: 0, MAX: 10},
        ]},
        
        # Measurements - up to 40
        {ID: 'MEA', MIN: 0, MAX: 40},
        
        # Pricing Information - up to 25
        {ID: 'CTP', MIN: 0, MAX: 25},
        
        # Terms of Sale/Deferred Terms of Sale - up to 2
        {ID: 'ITD', MIN: 0, MAX: 2},
        
        # Discount Detail - up to 20
        {ID: 'DIS', MIN: 0, MAX: 20},
        
        # Tax Reference - up to 99999
        {ID: 'TAX', MIN: 0, MAX: 99999},
        
        # F.O.B. Related Instructions - up to 99999
        {ID: 'FOB', MIN: 0, MAX: 99999},
        
        # Shipment/Delivery Schedule Quantity - up to 500
        {ID: 'SDQ', MIN: 0, MAX: 500},
        
        # Additional Item Data - up to 5
        {ID: 'IT3', MIN: 0, MAX: 5},
        
        # Tax Information - up to 99999
        {ID: 'TXI', MIN: 0, MAX: 99999},
        
        # Reference Identification - up to 99999
        {ID: 'REF', MIN: 0, MAX: 99999},
        
        # Administrative Communications Contact - up to 3
        {ID: 'PER', MIN: 0, MAX: 3},
        
        # Service, Promotion, Allowance, or Charge Information - up to 25
        {ID: 'SAC', MIN: 0, MAX: 25, LEVEL: [
            {ID: 'CUR', MIN: 0, MAX: 1},
        ]},
        
        # Commodity - up to 1
        {ID: 'IT8', MIN: 0, MAX: 1},
        
        # Sales Requirements - up to 1
        {ID: 'CSH', MIN: 0, MAX: 1},
        
        # Carrier Details (Quantity and Weight) - up to 1
        {ID: 'TD1', MIN: 0, MAX: 1},
        
        # Carrier Details (Routing Sequence/Transit Time) - up to 12
        {ID: 'TD5', MIN: 0, MAX: 12},
        
        # Carrier Details (Equipment) - up to 12
        {ID: 'TD3', MIN: 0, MAX: 12},
        
        # Carrier Details (Special Handling, or Hazardous Materials, or Both) - up to 5
        {ID: 'TD4', MIN: 0, MAX: 5},
        
        # Marks and Numbers - up to 10
        {ID: 'MAN', MIN: 0, MAX: 10},
        
        # Marking, Packaging, Loading - up to 200
        {ID: 'PKG', MIN: 0, MAX: 200},
        
        # Quantity - up to 99999
        {ID: 'QTY', MIN: 0, MAX: 99999},
        
        # Line Item Schedule - up to 200
        {ID: 'SCH', MIN: 0, MAX: 200, LEVEL: [
            {ID: 'TD1', MIN: 0, MAX: 2},
            {ID: 'TD5', MIN: 0, MAX: 12},
            {ID: 'TD3', MIN: 0, MAX: 12},
            {ID: 'TD4', MIN: 0, MAX: 5},
            {ID: 'REF', MIN: 0, MAX: 99999},
        ]},
        
        # Extended Reference Information - up to 1000
        {ID: 'N9', MIN: 0, MAX: 1000, LEVEL: [
            {ID: 'DTM', MIN: 0, MAX: 99999},
            {ID: 'MEA', MIN: 0, MAX: 40},
            {ID: 'MSG', MIN: 0, MAX: 1000},
            {ID: 'MTX', MIN: 0, MAX: 99999},
        ]},
        
        # Name/Address Loop - up to 200
        {ID: 'N1', MIN: 0, MAX: 200, LEVEL: [
            {ID: 'N2', MIN: 0, MAX: 2},
            {ID: 'N3', MIN: 0, MAX: 2},
            {ID: 'N4', MIN: 0, MAX: 1},
            {ID: 'REF', MIN: 0, MAX: 12},
            {ID: 'PER', MIN: 0, MAX: 3},
            {ID: 'DTM', MIN: 0, MAX: 1},
        ]},
        
        # Code Source Information - up to 99999
        {ID: 'LM', MIN: 0, MAX: 99999, LEVEL: [
            {ID: 'LQ', MIN: 1, MAX: 99999},
        ]},
    ]},
    
    # Transaction Totals - optional
    {ID: 'CTT', MIN: 0, MAX: 1},
    
    # Transaction Set Trailer - mandatory
    {ID: 'SE', MIN: 1, MAX: 1},
]},
]
