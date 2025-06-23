import ttkbootstrap as ttkb

def myStyles():
    # Initialize the style
    style = ttkb.Style()

    style.configure('customEntry.TEntry',
                relief="flat",  # Removes the border
                padding=5, 
                backgorund = 'lightblue',
                )

    # Create custom style for Labelframe to remove bottom, right, and left borders
    style.configure('customLabelframe.TLabelframe', padding=(0,0,0,20), background='#F1F1F1', labelmargins=0, borderwidth=0)  
    style.configure('customLabelframe.TLabelframe.Label', background='#F1F1F1')
    
    style.configure('MyCustomFrame.TFrame', background='#F1F1F1', padding=20)

    style.configure('headerLabel.TLabel', background='#ffe0b3')
    style.configure('headerBorder.TFrame', background='#ff9900')
    style.configure('custom.TPanedwindow', background="#C1C1C1")

    style.configure('bodyLabel.TLabel', background='#F1F1F1')


    style.configure("lblFrm.TLabelframe", labelmargins=0, background='#F1F1F1', labeloutside="True")
    style.configure("lblFrm.TLabelframe.Label", background='#F1F1F1')
    

    # Modern style for the button
    style.configure('posBtn.TButton', 
                    font=('Arial', 12, 'bold'),  # Modern font style
                    background='#007BFF',  # Background color
                    foreground='white',  # Text color (white)
                    padding=(30, 10),  # Padding around the text
                    relief='flat',  # Flat border for a sleek look
                    width=10,  # Set width to control button size
                    anchor='center')  # Center the text

    # Hover effect for button
    style.map('posBtn.TButton', 
              background=[('active', '#0056b3')],  # Darker blue when active
              foreground=[('active', 'white')])  # White text on hover
    
    # Modern style for the button
    style.configure('startBtn.TButton', 
                    font=('Arial', 18, 'bold'),  # Modern font style
                    background='#4CAF50',  # Background color (blue)
                    foreground='white',  # Text color (white)
                    padding=(30, 20),  # Padding around the text
                    relief='flat',  # Flat border for a sleek look
                    width=10,  # Set width to control button size
                    anchor='center')  # Center the text

    # Hover effect for button
    style.map('startBtn.TButton', 
              background=[('active', '#388E3C')],  # Darker blue when active
              foreground=[('active', 'white')])  # White text on hover
    
    # Modern style for the button
    style.configure('stopBtn.TButton', 
                    font=('Arial', 18, 'bold'),  # Modern font style
                    background='#F44336',  # Background color (blue)
                    foreground='white',  # Text color (white)
                    padding=(30, 20),  # Padding around the text
                    relief='flat',  # Flat border for a sleek look
                    width=10,  # Set width to control button size
                    anchor='center')  # Center the text

    # Hover effect for button
    style.map('stopBtn.TButton', 
              background=[('active', '#D32F2F')],  # Darker blue when active
              foreground=[('active', 'white')])  # White text on hover
    
    # Modern style for the button
    style.configure('reportBtn.TButton', 
                    font=('Arial', 12, 'bold'),  # Modern font style
                    background='#007BFF',  # Background color (blue)
                    foreground='white',  # Text color (white)
                    padding=(30, 10),  # Padding around the text
                    relief='flat',  # Flat border for a sleek look
                    width=12,  # Set width to control button size
                    anchor='center')  # Center the text

    # Hover effect for button
    style.map('reportBtn.TButton', 
              background=[('active', '#0056b3')],  # Darker blue when active
              foreground=[('active', 'white')])  # White text on hover
    
    # Create a custom style for Combobox
    style.configure('custom.TCombobox', background=[('disabled', 'white'), ('pressed !disabled', 'blue'),('focus !disabled', 'green'),('hover !disabled', 'yellow')], font=("Arial", 12), width=10)
    
    style.map('myRadBtn.TRadiobutton',
          background=[('active', '#F1F1F1')],
          indicatorcolor=[('selected', '#007BFF')])

    # radio button style
    style.configure('myRadBtn.TRadiobutton',
                compound='#007BFF',
                background="#F1F1F1",
                font=("Arial", 12))


    # Configure the light grey background for frames
    style.configure('TFrame', background='#F1F1F1')
    style.configure('headerFrame.TFrame', background='#ffe0b3')

    

    return style