﻿<%@ Page Title="" Language="C#" MasterPageFile="FeaturePage.master" AutoEventWireup="true"
    CodeFile="Studio.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Package for Linux
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="featurecontent" runat="Server">
    <div class="grid_10" style="width: 600px;">
        <h1>
            Create SUSE Powered Appliance</h1>
        <p>
            With SUSE Studio, you can bundle your application and a customized version of SUSE
            Linux into a fully configured, ready to go appliance.</p><br />
        <p>
            With everything packaged in a single virtual machine, distribution and setup is
            simple for both you and your users!</p>
        <br /><h2>Step 1:</h2>
        <p>
            Go to Mono -> Create SUSE Powered Appliance</p>
        <br /><img class="shot" src="img/appliance1.png" alt="Create SUSE Studio Appliance - Step 1" />
        <br /><h2>Step 2:</h2>
        <p>
            Enter your SUSE Studio username and API key.</p>
        <p class="note">
            Hint: If you don't have a SUSE Studio account, sign up for one <a href="http://susestudio.com/account/login">
                here</a>. If you have a SUSE Studio account but don't know your API key, get
            it <a href="http://susestudio.com/user/show_api_key">here</a>.</p>
        <br /><img class="shot" src="img/appliance2.png" alt="Create SUSE Studio Appliance - Step 2" />
        <br /><h2>Step 3:</h2>
        <p>
            You will be presented with a list of all your appliances available on SUSE Studio.
            Choose one that you wish to modify, or you can create a new one.</p>
        <br /><img class="shot" src="img/appliance3.png" alt="Create SUSE Studio Appliance - Step 3" />
        <br /><h2>Step 4:</h2>
        <p>
            Once you've selected the appliance to use, choose your Linux RPM package that you
            want to upload to the appliance.</p>
        <p class="note">
            Hint: If you haven't created a Linux installer package for your application, do
            that first with the <a href="Package.aspx">Create Package functionality</a>.
        </p>
        <br /><img class="shot" src="img/appliance5.png" alt="Create SUSE Studio Appliance - Step 5" />
        <br /><h2>Step 5:</h2>
        <p>
            Your appliance will be created and your package will be uploaded to the it. From
            here, you can go to the SUSE Studio website to further customize and build your
            appliance.</p>
        <br /><img class="shot" src="img/appliance6.png" alt="Create SUSE Studio Appliance - Step 6" />
        <br /><br /><br />
    </div>
</asp:Content>
