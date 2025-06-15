import java.util.HashMap;
import java.util.Map;

public class WordFrequencyCounter {

    public static void main(String[] args) {
        String text = "Hello world, this is a test. This world is beautiful. " +
                      "Let's test the word count functionality of this world.";

        // 移除非字母字符，并转换为小写
        String cleanedText = text.replaceAll("[^a-zA-Z ]", "").toLowerCase();

        // 按空格分割成单词数组
        String[] words = cleanedText.split("\\s+");

        Map<String, Integer> wordFrequencies = new HashMap<>();

        // 遍历单词并计数
        for (String word : words) {
            if (!word.isEmpty()) {
                wordFrequencies.put(word, wordFrequencies.getOrDefault(word, 0) + 1);
            }
        }

        System.out.println("文本中的词频统计结果:");
        // 打印结果
        for (Map.Entry<String, Integer> entry : wordFrequencies.entrySet()) {
            System.out.println("'" + entry.getKey() + "': " + entry.getValue() + " 次");
        }
    }
}