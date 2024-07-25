namespace TestDataGenerator.Models
{
    public class DropdownModel
    {
        public string SelectedValue { get; set; }
        public string SelectedLanguage { get; set; }  
        public int NumberOfData { get; set; }
        //public List<string> Options { get; set; }

        public Dictionary<string, string> Options { get;set; }
        public List<string> Languages { get; set; }
    }
}
