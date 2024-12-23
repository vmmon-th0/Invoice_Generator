#!/bin/bash

# Check if INVOICE_GEN_CONF is already defined
if [ -n "$INVOICE_GEN_CONF" ]; then
    echo "The environment variable INVOICE_GEN_CONF is already set to: $INVOICE_GEN_CONF"
    read -p "Do you want to replace it? [y/N]: " overwrite_conf
    if [[ "$overwrite_conf" != "y" && "$overwrite_conf" != "Y" ]]; then
        echo "Operation canceled."
        exit 1
    fi
fi

# Ask for the path to store the configuration file
read -p "Enter the destination path to store the configuration file: " conf_path

# Check if the path exists, otherwise offer to create it
if [ ! -d "$conf_path" ]; then
    read -p "The directory $conf_path does not exist. Do you want to create it? [y/N]: " create_dir
    if [[ "$create_dir" == "y" || "$create_dir" == "Y" ]]; then
        mkdir -p "$conf_path" || { echo "Failed to create the directory."; exit 1; }
    else
        echo "Cannot continue without a valid directory. Operation canceled."
        exit 1
    fi
fi

# Set the INVOICE_GEN_CONF environment variable
export INVOICE_GEN_CONF="$conf_path"
echo "INVOICE_GEN_CONF set to $INVOICE_GEN_CONF"

# Add INVOICE_GEN_CONF to the shell profile
read -p "Do you want to add INVOICE_GEN_CONF to your shell profile (~/.zshrc) ? [y/N]: " add_to_profile
if [[ "$add_to_profile" == "y" || "$add_to_profile" == "Y" ]]; then
    echo "export INVOICE_GEN_CONF=\"$conf_path\"" >> ~/.zshrc
    echo "INVOICE_GEN_CONF has been added to ~/.zshrc"
fi

# Path to the configuration file
conf_file="$conf_path/.invoice_gen_conf.ini"

# Check if the configuration file already exists
if [ -f "$conf_file" ]; then
    read -p "The configuration file already exists. Do you want to replace it? [y/N]: " overwrite_file
    if [[ "$overwrite_file" != "y" && "$overwrite_file" != "Y" ]]; then
        echo "Operation canceled."
        exit 1
    fi
fi

# Ask for the path to store invoices
read -p "Enter the path where invoices will be stored: " invoices_location

# Check if the invoices directory already exists
if [ -d "$invoices_location" ]; then
    read -p "The folder $invoices_location already exists. Do you want to use it anyway? [y/N]: " use_existing
    if [[ "$use_existing" != "y" && "$use_existing" != "Y" ]]; then
        echo "Operation canceled."
        exit 1
    fi
else
    mkdir -p "$invoices_location" || { echo "Failed to create the invoices folder."; exit 1; }
fi

# Create the configuration file
cat > "$conf_file" <<EOL
[path]
invoices_location = $invoices_location

[database]
db = WIP
EOL

echo "Configuration file created at $conf_file"
echo "Initialization completed successfully."
