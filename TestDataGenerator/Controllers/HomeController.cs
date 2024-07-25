using Microsoft.AspNetCore.Mvc;
using System;
using System.Diagnostics;
using TestDataGenerator.Models;
using static System.Net.Mime.MediaTypeNames;

namespace TestDataGenerator.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            var model = new DropdownModel();
            model.Options = new Dictionary<string, string>();

            model.Options.Add("Test", "Select..");
            model.Options.Add("wrapperdistinattachedeml", "Journal Email");
            model.Options.Add("emlfilecontainattachmnet", "Email file contain attachment");
            model.Options.Add("emlfilewithdetails", "Email file with details");
            model.Options.Add("emlfilewithdomainname", "Email file with domain name");
            model.Options.Add("voicewithmetadata", "Voice/Call");
            model.Options.Add("videowithmetadata", "Video/Mp4");

            model.Languages = new List<string>();
            model.Languages.Add("English");
            model.Languages.Add("Spanish");
            model.Languages.Add("French");
            model.Languages.Add("German");
            model.Languages.Add("Italian");
            model.Languages.Add("Portuguese");
            model.Languages.Add("Dutch");
            model.Languages.Add("Russian");
            model.Languages.Add("Chinese (Mandarin and Cantonese)");
            model.Languages.Add("Japanese");
            model.Languages.Add("Korean");

            string outputDirectory = TempData["OutputDirectory"] as string;
            string pythonError = TempData["PythonError"] as string;

            // Check if data is null to handle edge cases
            // Process and prepare data for display or handle errors

            // Pass data to the view
            ViewData["OutputDirectory"] = outputDirectory;
            ViewData["PythonError"] = pythonError;

            return View(model);
        }

        [HttpPost]
        public IActionResult SubmitForm(DropdownModel selectedOption)
        {
            CallPythonScript(selectedOption.SelectedValue, selectedOption.NumberOfData);
            return RedirectToAction("Index");
        }

        private void CallPythonScript(string seletedOption, int NumberOfData)
        {
            // Path to the Python executable
            string pythonPath = @"C:\Users\upal\AppData\Local\Programs\Python\Python312\python.exe";//@"C:\Python311\python.exe";// @"C:\Path\to\python.exe";
            //string pythonPath = "python";

            // Path to your Python script
            string scriptPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, $"PythonScripts\\{seletedOption}.py");

            // Create process info
            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = pythonPath;
            //psi.Arguments = $"\"{scriptPath}\"";
            psi.Arguments = $"{scriptPath} {NumberOfData}";

            // Redirect standard output for displaying results
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;

            // Start the process
            using (Process process = Process.Start(psi))
            {
                // Read the output (if needed)
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();

                    TempData["OutputDirectory"] = result;

                    Console.WriteLine("Output from Python script:");
                    Console.WriteLine(result);
                }
                // Check for errors
                using (StreamReader reader = process.StandardError)
                {
                    string error = reader.ReadToEnd();
                    if (!string.IsNullOrEmpty(error))
                    {
                        Console.WriteLine("Error from Python script:");
                        Console.WriteLine(error);

                        if (!string.IsNullOrEmpty(error))
                        {
                            TempData["PythonError"] = error;
                        }
                    }
                }
            }
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}