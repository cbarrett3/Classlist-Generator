# --------------------------------------------------------------------------------
# Authors:      Connor Barrett
# Project:      Classlist Algorithm
# Purpose:      To create Classlists as even as possible given certain requirements
# --------------------------------------------------------------------------------
import pandas as pd


class ClasslistCreation:
	def __init__(self, filename):
		# read first 9 columns of xlsx into a pandas dataframe
		self.kids = pd.read_excel('uploads/' + filename, usecols=9)
		# save names of teachers for the end
		self.teacher_names = list(self.kids['Please List All Future Teacher Names Here'])
		self.teacher_names = [x for x in self.teacher_names if str(x) != 'nan']
		# drops un-needed column from kids
		self.kids = self.kids.drop(labels='Please List All Future Teacher Names Here', axis=1)
		# initialize empty dictionary to hold all future classlists
		self.classlists = {}
		# initialize empty df's for each future teacher's classlist
		for teacher in self.teacher_names:
			self.classlists[teacher] = pd.DataFrame()
		# count total number of students we are working with (used in generator)
		self.num_students = len(self.kids)
		# count total number of teacher we are working with (used in generator)
		self.num_teachers = len(self.teacher_names)

	def early_placement(self):
		for index, row in self.kids.iterrows():
			# checks if a specific future teacher has been requested
			if pd.notnull(row["Future Teacher Last Name (N/A If Unknown)"]):
				# save student's row into it's own dataframe so we can append it
				df = pd.DataFrame().append(row)
				# append student's row into the requested teacher's classlist
				self.classlists[str(row["Future Teacher Last Name (N/A If Unknown)"])] = \
					self.classlists[str(row["Future Teacher Last Name (N/A If Unknown)"])].append(df, ignore_index=True)
				# drop this student's row from the kids df because placement is final
				self.kids = self.kids.drop([index])
		# update indices of rows in kids df
		self.kids = self.kids.reset_index(drop=True)
		# return classlists
		return self.classlists

