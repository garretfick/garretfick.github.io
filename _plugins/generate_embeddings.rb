module Jekyll
  Hooks.register :site, :post_write do |site|
    puts "Generating embeddings..."
    result = system("python3 ./generate_embeddings.py")
    if result
      puts "✅ Embeddings generated successfully"
    else
      puts "❌ Failed to generate embeddings"
    end
  end
end