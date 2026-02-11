module Jekyll
  Hooks.register :site, :post_write do |site|
    puts "Generating embeddings..."
    result = system("python3 ./generate_embeddings.py")
    unless result
      raise "Embedding generation failed"
    end
    puts "Embeddings generated successfully"
  end
end