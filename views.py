# myapp/views.py
import pandas as pd
from django.shortcuts import render
from myApp.forms import UploadFileForm
import matplotlib.pyplot as plt
import io
import base64

def home(request):
    return render(request, 'home.html')

def upload_file(request):
    data_preview = None
    error_message = None
    plot_url = None  # Initialize plot_url
   
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()

            try:
                file_path = uploaded_file.file.path
                df = pd.read_csv(file_path)                
                if 'Country Name' in df.columns :
                    for cl in df.columns:
                      if cl=='2019':
                       cl='2019' 
                    # Create a histogram for the 'value' column
                    mean_value = df[cl].mean()
                    median_value = df[cl].median()
                    fig, ax = plt.subplots()
                    df[cl].plot(kind='hist', ax=ax, bins=20)
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    plt.close(fig)
                    buf.seek(0)
                    plot_url = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')
                # Debug: Print DataFrame columns
                # print("DataFrame Columns:", df.columns)

                # # Check if necessary columns exist
                
                # if 'Country Name' in df.columns :
                #     for cl in df.columns:
                #       if cl=='2019':
                #        cl='2019' 
                #        grouped_data = df[cl]
                        
                #     # Generate a bar plot for 'value' grouped by 'year'
                   

                #     # Ensure grouped_data is a Series
                #     print("Grouped Data Type:", type(grouped_data))

                #     # Generate and save the bar plot to an in-memory object
                    
                #     plt.hist(grouped_data)
                #     buf = io.BytesIO()
                #     plt.savefig(buf, format='png')
                    
                #     buf.seek(0)
                #     plot_url = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')

                    data_preview = df.head().to_html()
                else:
                    error_message = "The necessary columns ('year' and 'value') do not exist in the uploaded CSV file."
            
            except Exception as e:
                error_message = str(e)

            return render(request, 'upload_success.html', {
                'data_preview': data_preview, 
                'error_message': error_message, 
                'plot_url': plot_url,
                'mean_value': mean_value,
                'median_value': median_value,
            })
        else:
            error_message = "Form is not valid. Please check the uploaded file."
            return render(request, 'upload_form.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadFileForm()
        return render(request, 'upload_form.html', {'form': form, 'error_message': "Unexpected error. Please try again."})
    # Fallback return statement (this should ideally never be reached)
    

def upload_success(request):
    return render(request, 'upload_success.html')
