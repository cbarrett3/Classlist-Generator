# --------------------------------------------------------------------------------
# Authors:      Connor Barrett
# Project:      Classlist Algorithm
# Purpose:      To create Classlists as even as possible given certain requirements
# --------------------------------------------------------------------------------
import pandas as pd
import numpy as np


class Generator:
	def __init__(self, classlists, kids, num_students, num_teachers):
		# dictionary of classlist df's which we will be adding to (early placement already done)
		self.classlists = classlists
		# adding 'Candidate Score' column to each teacher's df
		for teacher in self.classlists:
			self.classlists[teacher]['Candidate Score'] = np.nan
		# df of kids which still need to be placed
		self.kids = kids
		# adding 'Candidate Score' column to kids df
		self.kids['Candidate Score'] = np.nan
		# total number of students in initial spreadsheet
		self.num_students = num_students
		# counter to keep track of the number of students placed
		self.students_placed = 0
		# number of teachers to make future classlists for
		self.num_teachers = num_teachers
		# best candidate score initialization
		self.best_score = 0
		# dataframe to hold best candidate information
		self.ideal_candidate_df = pd.DataFrame()
		# index of student to drop from kids
		self.index_to_drop = 0

	def generate(self):
		# while not all students have been placed
		while self.students_placed < self.num_students:
			# loop through future teacher classlists, placing the best candidate for that teacher's class each time
			for teacher in self.classlists:
				# Level 4 Priority: factor in class sizes
				# check if class even needs another student and if not, skip this teacher
				max_class_size = (self.num_students / self.num_teachers)
				if self.classlists[teacher].shape[0] > max_class_size:
					continue
				# loop through each student (index) in kids and calculate their score, keeping track of the best
				for index, row in self.kids.iterrows():
					# save student's row into it's own dataframe so we can append it
					df = pd.DataFrame().append(row)
					# append student's row (df) into the requested teacher's classlist
					self.classlists[teacher] = self.classlists[teacher].append(df, ignore_index=True, sort=False)

					# Calculate Candidate Score

					# Level 3-4 Priority: factor in academic, behavior, and communication ratings
					# find lowest total between academic, behavior, and communication to adjust weight
					a_total = self.classlists[teacher]["Academic Score (1-5)"].sum()
					b_total = self.classlists[teacher]["Behavior Score (1-5)"].sum()
					c_total = self.classlists[teacher]["Communication Score (1-3)"].sum()
					# place heavier weight by 1 on area that is the lowest in the current class
					if a_total < b_total and a_total < c_total:
						candidate_score = row["Academic Score (1-5)"] * 4 + row["Behavior Score (1-5)"] * 3 + row["Communication Score (1-3)"] * 3
					elif b_total < a_total and b_total < c_total:
						candidate_score = row["Academic Score (1-5)"] * 3 + row["Behavior Score (1-5)"] * 4 + row["Communication Score (1-3)"] * 3
					elif c_total < a_total and b_total:
						candidate_score = row["Academic Score (1-5)"] * 3 + row["Behavior Score (1-5)"] * 3 + row["Communication Score (1-3)"] * 4
					else:
						candidate_score = row["Academic Score (1-5)"] * 3 + row["Behavior Score (1-5)"] * 3 + row["Communication Score (1-3)"] * 3

					# Level 4 Priority: Factor in number in same class previously
					max_number_in_previous = max(self.classlists[teacher].groupby('Teacher Last Name').size())
					# majorly violates, decrease score by 90%
					if max_number_in_previous > 6:
						candidate_score *= .1
					# violates, decrease score by 70%
					elif max_number_in_previous > 5:
						candidate_score *= .3

					# Level 4 Priority: Factor in gender
					most_common_gender = self.classlists[teacher]['Student Gender (M/F)'].value_counts().idxmax()
					# lessen score if this student belongs to the  most common gender in the class
					if row['Student Gender (M/F)'] == most_common_gender:
						candidate_score *= .3

					# Check if a new ideal candidate has been found
					if candidate_score > self.best_score:
						# update new best score (ideal candidate)
						self.best_score = candidate_score
						# clear out current ideal candidate from ideal candidate df
						self.ideal_candidate_df.drop(self.ideal_candidate_df.index, inplace=True)
						# add new ideal candidate to ideal candidate df
						self.ideal_candidate_df = self.ideal_candidate_df.append(df)
						# save this index so we can drop the correct student from kids later
						self.index_to_drop = index
					# drop student's row (df) from the requested teacher's classlist
					self.classlists[teacher].drop(self.classlists[teacher].tail(1).index, inplace=True)
					# drop student's row from it's own dataframe so we can reuse 'df' (reset df)
					df.drop(df.index, inplace=True)
				# best_score found, append that row into current teachers class
				self.classlists[teacher] = self.classlists[teacher].append(self.ideal_candidate_df, ignore_index=True, sort=False)
				# update counter
				self.students_placed += 1
				print(self.students_placed)
				# check if kids is empty
				if self.kids.empty:
					return self.classlists
				# drop this student's row from the kids df because placement is final
				self.kids = self.kids.drop([self.index_to_drop])
				# print(self.index_to_drop)
				# update indices of rows in kids df
				self.kids = self.kids.reset_index(drop=True)
				# reset best score
				self.best_score = 0
		# return classlists
		return self.classlists
