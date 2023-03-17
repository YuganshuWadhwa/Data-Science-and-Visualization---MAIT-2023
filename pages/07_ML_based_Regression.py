import streamlit as st
import pandas as pd

# import necessary class definitions from relevant packages
from GUI.GUI_Class import GUI_class
from ML_Regression.Regression import Regression


# Setup for page configuration
st.set_page_config(
	page_title = 'ML based Regression',
	layout = 'wide'
	)


header_cont = st.container()


with header_cont :
	st.markdown("<h2 style = 'text-align : center; color : #0077b6;'> REGRESSION </h2>", unsafe_allow_html = True)

	st.markdown("<h5 style = 'text-align : center; color : #023e8a;'> SVM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Gradient Boosting &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Decision Tree </h5>", unsafe_allow_html = True)

	st.markdown(':bulb: <small> <i> :orange[Regression models work best with Time-series type datasets.] </i> </small>', unsafe_allow_html = True)

	st.markdown('# ')



# providing the choice to use original dataframe or processed dataframe
working_df_choice = st.selectbox(label = 'df', options = ['Select Dataset to Proceed :', 'Original Dataset', 'Processed Dataset after performing Outlier Recognition, Interpolation and Smoothening'], index = 0, label_visibility = 'collapsed')

if working_df_choice == 'Original Dataset' :
	# loading original dataframe from cache
	working_df = st.session_state['GUI_data'].data
	st.dataframe(working_df)
	st.markdown('# ')


elif working_df_choice == 'Processed Dataset after performing Outlier Recognition, Interpolation and Smoothening' :

	try :
		# loading processed dataframe from cache
		working_df = st.session_state['smoothed_df']
		st.dataframe(working_df)
		st.markdown('# ')

	except :
		# exception handling
		st.markdown(':exclamation: <small> <i> :orange[Please generate processed data using previous pages, or select "Original Dataset" option] </i> </small>', unsafe_allow_html = True)
		working_df = None
		
else :
	working_df = None


if working_df is not None : 

	inputs_cont = st.container()

	with inputs_cont :

		# initializing class object
		Regression_object = Regression(working_df)

		st.markdown('# ')

		# user-inputs for generating training and test data
		st.markdown("<h5 style = 'text-align : left; color : #0096c7;'> Constructing Training and Testing Data : </h5>", unsafe_allow_html = True)
		st.markdown('#### ')


		test_col_4, dummy_col_2, test_col_5 = st.columns([2, 0.5, 2])

		test_col_4.markdown('Select ***Target Attribute*** from the dataset to ***Predict*** : ', unsafe_allow_html = True)
		label_target = test_col_4.selectbox(label = 'lt', options = list(working_df.columns), index = 1, label_visibility = 'collapsed')
		st.markdown('#### ')

		test_col_5.markdown('Select ***Percentage*** of complete data to be used for ***Testing*** :', unsafe_allow_html = True)
		testsize = test_col_5.slider(label = 'ts', min_value = 20, max_value = 70, value = 30, step = 10, label_visibility = 'collapsed')


		test_col_6, dummy_col_3 ,test_col_7, dummy_col_4, test_col_8, dummy_col_100, test_col_100 = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1])

		test_col_6.markdown('***Delete NULL values*** from the data', unsafe_allow_html = True)
		deleting_na = test_col_6.checkbox(label = 'dn', value = False, label_visibility = 'collapsed')
		st.markdown('# ')


		test_col_7.markdown('***Scaling***', unsafe_allow_html = True)
		scaling = test_col_7.checkbox(label = 's', value = False, label_visibility = 'collapsed')
		st.markdown('# ')


		test_col_8.markdown('***Delete Duplicates***', unsafe_allow_html = True)
		deleting_duplicates = test_col_8.checkbox(label = 'dd', value = False, label_visibility = 'collapsed')

		test_col_100.markdown('***Remove Noise***', unsafe_allow_html = True)
		remove_noise = test_col_100.checkbox(label = 'rn', value = False, label_visibility = 'collapsed')

		test_col_101, dummy_col_101, test_col_102 = st.columns([1, 0.2, 1])

		rows_to_keep = test_col_101.slider(label = 'Select Rows to Keep', min_value = 0, max_value = len(working_df), value = 16000, step = 1)
		cols_to_keep = test_col_102.multiselect(label = 'Select Columns to Keep', options = list(working_df.columns), default = list(working_df.columns))

		# calling class method to generate training and testing data
		Regression_object.split_train_test(label_target = label_target, 
										rows_to_keep = rows_to_keep,
										testsize = testsize/100., 
										random_state = 1, 
										deleting_na = deleting_na, 
										scaling = scaling, 
										deleting_duplicates = deleting_duplicates,
										remove_noise = remove_noise,
										cols_to_keep = cols_to_keep)



		# selection of method
		choice_text, choice_box = st.columns([1, 2])

		choice_text.markdown('Select Regression Model :')
		method = choice_box.selectbox(label = '', label_visibility = 'collapsed', options = ['Support Vector Machine Regression', 'Gradient Boosting Regression', 'Decision Tree'], index = 0)


		if method == 'Support Vector Machine Regression' :

			test_col_9, dummy_col_5, test_col_10, dummy_col_6, test_col_11 = st.columns([1, 0.2, 1, 0.2, 1])
			test_col_103, dummy_col_7, test_col_12 = st.columns([1, 0.2, 1])

			kernel = test_col_9.selectbox(label = 'Select kernel', options = ['linear', 'poly', 'rbf', 'sigmoid'], index = 2)
			degree = test_col_10.slider(label = 'Select degree', min_value = 0, max_value =10, value = 3)
			svmNumber = test_col_11.slider(label = 'Select svmNumber', min_value = 0, max_value =10, value = 500, step = 10)

			maxIterations = test_col_12.slider(label = 'Select maxIterations', min_value = -1, max_value =15000, value = -1)
			epsilon = test_col_103.slider(label = 'Select epsilon', min_value = 0.1, max_value =1., value = 0.5, step = 0.1)


			# checkbox to begin training
			test_col_13, dummy_col_8, test_col_14 = st.columns([3, 0.2, 1.5])

			test_col_13.markdown(':bulb: <small> <i> :orange[Click the checkbox to build the regression model. This process can take a few minutes.<br>While changing the model parameters, uncheck the box, change the parameters, then check the box again.] </i> </small>', unsafe_allow_html = True)

			build_model = test_col_14.checkbox(label = 'Build Regression Model')

			if build_model :
				Regression_object.build_regression(regression_name = method,
											kernel = kernel, 
											degree = degree, 
											svmNumber = svmNumber, 
											epsilon = epsilon,
											maxIterations = maxIterations)


		elif method == 'Gradient Boosting Regression' :

			test_col_9, dummy_col_5, test_col_10, dummy_col_6, test_col_11 = st.columns([1, 0.2, 1, 0.2, 1])
			test_col_103, dummy_col_7, test_col_12 = st.columns([1, 0.2, 1])

			alpha = test_col_9.slider(label = 'Select alpha', min_value = 0.1, max_value = 1.)
			max_depth = test_col_10.slider(label = 'Select max_depth', min_value = 10, max_value = 1000)
			min_samples_leaf = test_col_11.slider(label = 'Select min_samples_leaf', min_value = 10, max_value = 100)

			n_estimators = test_col_12.slider(label = 'Select n_estimators', min_value = 100, max_value = 1000)
			learning_rate = test_col_103.slider(label = 'Select learning_rate', min_value = 0.1, max_value =1.)


			# checkbox to begin training
			test_col_13, dummy_col_8, test_col_14 = st.columns([3, 0.2, 1.5])

			test_col_13.markdown(':bulb: <small> <i> :orange[Click the checkbox to build the regression model. This process can take a few minutes.<br>While changing the model parameters, uncheck the box, change the parameters, then check the box again.] </i> </small>', unsafe_allow_html = True)

			build_model = test_col_14.checkbox(label = 'Build Regression Model')

			if build_model :
				Regression_object.build_regression(regression_name = method,
											alpha = alpha, 
											max_depth = max_depth, 
											min_samples_leaf = min_samples_leaf, 
											n_estimators = n_estimators,
											learning_rate = learning_rate)


		elif method == 'Decision Tree' :

			test_col_10, dummy_col_6, test_col_11 = st.columns([1, 0.2, 1])
			test_col_103, dummy_col_7, test_col_12 = st.columns([1, 0.2, 1])

			max_depth = test_col_10.slider(label = 'Select max_depth', min_value = 10, max_value =1000)
			min_samples_leaf = test_col_11.slider(label = 'Select min_samples_leaf', min_value = 1, max_value =10)

			min_samples_split = test_col_12.slider(label = 'Select min_samples_split', min_value = 2, max_value =10)
			max_leaf_nodes = test_col_103.slider(label = 'Select max_leaf_nodes', min_value = 2, max_value = 2000)


			# checkbox to begin training
			test_col_13, dummy_col_8, test_col_14 = st.columns([3, 0.2, 1.5])

			test_col_13.markdown(':bulb: <small> <i> :orange[Click the checkbox to build the regression model. This process can take a few minutes.<br>While changing the model parameters, uncheck the box, change the parameters, then check the box again.] </i> </small>', unsafe_allow_html = True)

			build_model = test_col_14.checkbox(label = 'Build Regression Model')
			
			if build_model :
				Regression_object.build_regression(regression_name = method,
											max_depth = max_depth, 
											min_samples_leaf = min_samples_leaf, 
											min_samples_split = min_samples_split,
											max_leaf_nodes = max_leaf_nodes)


	if build_model :
		result_cont = st.container()

		with result_cont:
			
			st.markdown('# ')
			st.markdown("<h5 style = 'text-align : left; color : #0096c7;'> Results : </h5>", unsafe_allow_html = True)

			Regression_object.plot_test_data()
			Regression_object.plot_train_data()

			st.pyplot(Regression_object.fig_test)
			st.pyplot(Regression_object.fig_train)

			st.markdown('# ')
			st.markdown("<h5 style = 'text-align : left; color : #0096c7;'> Test The Model : </h5>", unsafe_allow_html = True)

			test_file = st.file_uploader(label = 'Upload Test Dataset in .csv Format', type = ['csv'])

			if test_file is not None :
				test_data = pd.read_csv(test_file, sep=';|,', engine='python')
				st.write(test_data)
				Regression_object.regression_function(test_data)

			else :
				test_data = pd.DataFrame()